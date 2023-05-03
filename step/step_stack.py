from constructs import Construct
from aws_cdk import (
    Duration,
    Stack,
    aws_iam as iam,
    aws_sqs as sqs,
    aws_sns as sns,
    aws_sns_subscriptions as subs,
    aws_stepfunctions as sfn,
    aws_stepfunctions_tasks as tasks,
    aws_lambda as lambda_,
    aws_events as events,
    aws_events_targets as targets,
)


class StepStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        hello_function = lambda_.Function(self, "MyLambdaFunction",
                                          code=lambda_.Code.from_inline("""
                                exports.handler = (event, context, callback) => {
                                    callback(null, "Hello World!");
                                }"""),
                                          runtime=lambda_.Runtime.NODEJS_12_X,
                                          handler="index.handler",
                                          timeout=Duration.seconds(25))

        state_machine = sfn.StateMachine(self, "MyStateMachine",
                                         definition=tasks.LambdaInvoke(self, "MyLambdaTask",
                                            lambda_function=hello_function).next(
                                            sfn.Succeed(self, "GreetedWorld"))) 

        event = events.Rule(self, "ScheduleRule",
                            # default fror this cron method will just give every minute
                            schedule=events.Schedule.cron(),
        )

        event.add_target(targets.SfnStateMachine(machine=state_machine))
