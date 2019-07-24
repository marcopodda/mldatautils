from pathlib import Path

from mlutils.core.logging import Logger
from mlutils.core.event.handler import EventHandler


class ModelSaver(EventHandler):
    def __init__(self, path=Path('mlutils/ckpts'), monitor='validation_loss'):
        self.path = path
        self.monitor = monitor
        self.logger = Logger()

    def on_fit_end(self, state):
        filename = self.path / "last.pt"
        self.logger.info(f"Saving last model in {filename}")
        state.save(filename)

    def on_epoch_end(self, state):
        if state.best_results[self.monitor]['best_epoch'] == state.epoch:
            filename = self.path / "best.pt"
            self.logger.info(f"Found new best model at epoch {state.epoch}. Saving in {filename}")
            state.save(filename)
