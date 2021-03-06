#!/usr/bin/env python2.7
# Entry point script for cloud version AClib
from __future__ import print_function
import sys
import os
import argparse
from cloud import events
import multiprocessing
from cloud.config import Config
import install_scenario  # pylint: disable=f0401
import run_scenario as runner  # pylint: disable=f0401

__aclib_root__ = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


def main():
    '''Start several AClib experiments with a provided runconfig file'''
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'config',
        type=argparse.FileType('r', 0),
        default=sys.stdin)
    args = parser.parse_args()

    config = Config()
    config.load(args.config)
    config.expand()
    errors = config.check()
    if errors:
        errors.insert(0, 'Error in configuration')
        print('\n'.join(errors))
        print('Complete configuration:')
        print(config)
    success_events = [events.SuccessMail(config.emails), events.Shutdown()]
    failure_events = [events.FailMail(config.emails)]

    # Semaphore to allow a maximum number of parallel running experiments
    parallel_run_block = multiprocessing.Semaphore(config.parallel_runs)
    # Mutex to avoid experiments installing at the same time
    install_mutex = multiprocessing.Lock()

    # Create experiment processes
    run_processes = [ExperimentRunner(exp, parallel_run_block, install_mutex,
                                      failure_events)
                     for exp in config.experiments]

    # Start experiments
    for process in run_processes:
        parallel_run_block.acquire()
        process.start()

    # Wait until processes finish or for user interrupt
    try:
        map(ExperimentRunner.join, run_processes)
    except KeyboardInterrupt:
        print("\nExiting due to user interrupt", file=sys.stderr)
        sys.exit(1)

    for e in success_events:
        e()


class ExperimentRunner(multiprocessing.Process):
    '''Run an experiment in AClib in encapsulated in an own process'''
    def __init__(self, experiment, end_event, install_mutex, failure_events):

        multiprocessing.Process.__init__(self, name=experiment.name)

        self.install_mutex = install_mutex
        self.release_on_exit = end_event
        self.config = experiment
        self.failure_events = failure_events

    configurators = {
        'ParamILS': runner.ParamILSRunner,
        'SMAC': runner.SMACRunner,
        'irace': runner.IRaceRunner
    }

    def run(self):
        # Install scenario
        with self.install_mutex:
            print('Initializing experiment {}'.format(self.name))
            config_file = os.path.join(
                __aclib_root__,
                self.config.config_file)
            installer = install_scenario.Installer(config_file)
            installer.install_single_scenario(self.config.scenario)

            configurator = self.configurators[self.config.configurator](
                config_file,
                self.config.scenario,
                __aclib_root__,
                self.name)

            if self.config.validate and self.config.validate.mode == "TIME":
                configurator.prepare(
                    self.config.seed,
                    max_timestamp=self.config.validate.max,
                    min_timestamp=self.config.validate.min,
                    mult_factor=self.config.validate.factor)
            else:
                configurator.prepare(self.config.seed)

        # Run scenario
        try:
            if not self.config.only_prepare:
                print('Starting experiment {}'.format(self.name))
                configurator.run_scenario()
                if self.config.validate:
                    print('Starting validation {}'.format(self.name))
                    self.config.run_validate(
                        mode=self.config.validate.mode,
                        val_set=self.config.validate.set)
        except (KeyboardInterrupt, SystemExit):
            for e in self.failure_events:
                e()
            configurator.cleanup()
        finally:
            print('Experiment {} finished'.format(self.name))
            self.release_on_exit.release()

if __name__ == '__main__':
    main()
