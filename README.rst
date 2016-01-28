========================
AWTY - are we there yet?
========================


A library that holds progress state in a hierarchical construct.
Can be used to track overall progress of long running distributed computations
(or quick and local. whatever).

Comes with backends to render pretty progress bars.

It concerns itself with:

* composability: take the awty progress of a subsystem and integrate it into
  the overall progerss of a higher level system.

* different granularity of progress
  * 'ready', 'in progress', 'done'
  * 'ready', '1 of 10', '2 of 10', '3 of 10', ...,  'done'
  * 'ready', '5%', '20%', '80%', '99%', '99%', '99%', '99%', 'done'

* the "weight" of a progress or progress group. If you know one thing usually
 takes double as long as the other, you can give one a weight of 1 and the
 other of 2. The combined progress will then be as accurate as possible.
* different backends to save the progress to (in memory, redis)
* transport to communicate state updates (json, json over amqp,
  json over redis channel)

* fancy things to show in the ui:

  * text of current thing the progress is doing ("installing package X")
  * prediction: this usually takes x minutes



Usage
=====


```
def install_all_dependencies(dependencies):
    progress = FixedAmountProgress(amount=len(dependencies))
    progress.start()  # changes from 'new' to 'progressing'
    for dependency in dependencies:
        progress.label = 'installing {}'.format(dependency)
        install_dependency(dependency)
        progress.next_step()  # or progress.step = x

```
