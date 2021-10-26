# Security

Security with NaaS APIs uses security policies which are divided into two distinct parts, policy evaluation and policy enforcement. 

**Policy Evaluation** - Evaluates the input data and makes a determination based on the policy whether the input data 

**Policy Enforcement** - Enforcement of the policy is performing a set of actions based on the outcome of the evaluation

## Std library
**proprietary** - There is no library that is imported that performs the policy evaluation or policy enforcement. Instead the input data (such as REST calls) are sent to an OPA server for policy evaluation. The user then has to write the policy enforcement on each call.

## Policy Evaluator
[Open Policy Agent](https://www.openpolicyagent.org/docs/latest/) - The policy written in the `./policies` directory is what is used to evaluate user input. More information on how to run this is provided in the [security]() documentation