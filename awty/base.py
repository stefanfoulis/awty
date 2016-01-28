# -*- coding: utf-8 -*-
import json
from collections import OrderedDict


class ProgressBase(object):
    """
    Basic interface for Progress types.
    It encapsulates:
    'new' state: we know this progress exists
    'progressing' state: it's in progress (x%)
    'done' state: it's done (100%)

    Why so many states? Mainly for presentational purposes.
    Visually 0% done is not the same as "new".

    "progress": a number between 0 and 1
    """

    def __init__(self, state='new', progress=None, label=''):
        self.state = state
        self.progress = progress
        self.label = label

    def state(self):
        """return either 'new', 'progressing', or 'done'"""
        raise NotImplementedError

    def progress(self):
        """return the progress a floating number between 0 and 1"""
        raise NotImplementedError

    def label(self):
        """a short label for this progress for visual presentation"""
        raise NotImplemented

    def current_activity(self):
        """a short string representing what the things is doing right now"""
        raise NotImplemented

    def pretty_progress(self):
        """
        a string representing the progress in a human readable form
        e.g "55%" or "4 of 10"
        """
        raise NotImplemented

    def as_dict(self):
        return {
            'state': self.state,
            'progress': self.progress,
            # ...
        }

    def as_json(self):
        return json.dumps(self.as_dict(), sorted=True)


class PercentageProgress(ProgressBase):
    """
    progress in percent
    """
    pass


class FixedAmountProgress(ProgressBase):
    """
    has a known amount of steps.
    """
    pass


class BinaryProgress(ProgressBase):
    """
    it's either done or not.
    """
    pass


class ProgressContainerBase(ProgressBase):
    """
    same as progress, but holds the combined progress of all its children
    """

    def __init__(self, children=None):
        self._children = children if children is not None else OrderedDict({})

    @property
    def state(self):
        if not self.children():
            return 'done'
        elif all([x == 'new' for x in self.children()]):
            return 'new'
        elif all([x == 'done' for x in self.children()]):
            return 'done'
        # elif any([x == 'progress' for x in self.children()]):
        #     return 'progress'
        # at this point there are none with 'progress' and it's not purely
        # 'new' and not purely 'done'. So it can only be a mixture of
        # 'new' and 'done'.
        else:
            return 'progress'

    def register_subprogress(self, progress, weight=None):
        weight = weight if weight is not None else 1
        self._progresses[progress] = weight


class FixedAmountProgressContainer(ProgressContainerBase):
    """
    behaves like FixedAmountProgress, where each sub-progress is a step
    """
    pass


class PercentageProgressContainer(ProgressContainerBase):
    """
    behaves like PercentageProgress, where is shows progress calculated as
    percentage.
    """
