"""Progress tracker utility for batch tasks."""

import time
import logging

logger = logging.getLogger(__name__)


class ProgressTracker:
    """Tracks batch execution timing and ETA."""

    def __init__(self, total_steps: int, desc: str = "Task"):
        self.total_steps = total_steps
        self.desc = desc
        self.start_time = time.time()
        self.current_step = 0

    def update(self, steps: int = 1) -> None:
        self.current_step += steps
        elapsed = time.time() - self.start_time
        pct = (self.current_step / self.total_steps) * 100
        eta = (elapsed / self.current_step) * (self.total_steps - self.current_step) if self.current_step > 0 else 0
        if self.current_step % max(1, (self.total_steps // 5)) == 0 or self.current_step == self.total_steps:
            logger.info(f"[{self.desc}] Progress: {pct:.1f}% ({self.current_step}/{self.total_steps}) | ETA: {eta:.1f}s")
