from mamba import description, before, context, it

from doublex import Spy
from expects import expect, be_true, be_false
from doublex_expects import have_been_called, have_been_called_with

from mamba import reporter, runnable
from mamba.example import Example
from mamba.example_group import ExampleGroup

from spec.object_mother import an_example_group

TAGS = ['any_tag']

with description('Example execution using tags') as self:
    with before.each:
        self.reporter = Spy(reporter.Reporter)
        self.example_group = an_example_group()
        self.example_with_tags = Example(lambda x: x,
                                         parent=self.example_group,
                                         tags=TAGS)
        self.other_example = Example(lambda x: x, parent=self.example_group)

    with context('when tag is included in example tags'):
        with it('executes example'):
            self.example_with_tags.execute(self.reporter,
                                           runnable.ExecutionContext(),
                                           tags=TAGS)

            expect(self.example_with_tags.was_run).to(be_true)

    with context('when tag is not included in example tags'):
        with it('does not execute example'):
            self.other_example.execute(self.reporter,
                                       runnable.ExecutionContext(),
                                       tags=TAGS)

            expect(self.other_example.was_run).to(be_false)

    with context('when tag is included in example_group tags'):
        with before.each:
            self.example_group = ExampleGroup('any example_group', tags=TAGS)

            self.example = Example(lambda x: x)
            self.other_example = Example(lambda x: x)

        with it('executes children'):
            self.example_group.append(self.example)
            self.example_group.append(self.other_example)

            self.example_group.execute(self.reporter,
                                       runnable.ExecutionContext(),
                                       tags=TAGS)

            expect(self.example.was_run).to(be_true)
            expect(self.other_example.was_run).to(be_true)

        with it('executes example group too'):
            self.other_example_group = ExampleGroup('any example_group')

            self.other_example_group.append(self.example)
            self.other_example_group.append(self.other_example)

            self.example_group.append(self.other_example_group)

            self.example_group.execute(self.reporter,
                                       runnable.ExecutionContext(),
                                       tags=TAGS)

            expect(self.example.was_run).to(be_true)
            expect(self.other_example.was_run).to(be_true)

    with context('when example group does not have tags and silbing one does'):
        with it('skips example group without tags'):
            self.parent = ExampleGroup('any example_group')

            self.child = ExampleGroup('child example_group', tags=TAGS)
            self.example = Example(lambda x: x)
            self.child.append(self.example)

            self.silbing = ExampleGroup('silbing example_group')
            self.silbing.append(Example(lambda x: x))

            self.parent.append(self.child)
            self.parent.append(self.silbing)

            self.parent.execute(self.reporter,
                                runnable.ExecutionContext(),
                                tags=TAGS)

            expect(self.reporter.example_group_started).\
                to(have_been_called.twice)
            expect(self.reporter.example_group_started).\
                to(have_been_called_with(self.parent))
            expect(self.reporter.example_group_started).\
                to(have_been_called_with(self.child))