#!/usr/bin/env python3

import aws_cdk as cdk

from step.step_stack import StepStack


app = cdk.App()
StepStack(app, "step")

app.synth()
