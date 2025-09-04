
# UIUC CS443 Reinforcement Learning - Course Notes

I have had some knowledge in RL but forgot too much after the graduation of my master, so I followed the materials in the below link to catch up.

[Course Link](https://nanjiang.cs.illinois.edu/cs443/)

## C1: Introduction

### Markov Decision Process

A Markov decision process is a 4-tuple $(S,A,P_{a},R_{a})$
$S$: state
$A$: action
$P_a$: transition. $P(S_(t+1)|S_t, a_t)$ (So action has control over transition)
$R_{a}$: immediate reward $R_s^a = E[R_(t+1)|S_t=s, A_t=a]$

MDP assumes the future depends on the present and not the past.

Q1: but the current state can be represented using the past information?

Q2: why the reward function is designed as expectation that thus is independent with the past? Can it be a matrix $R(S_(t+1),S_t, A_t)$? Using expectation will ignore an optimal path to {S_t} from some {S_(t-1)^k} though rewards from {S_{t-1}^!k} are extreme low. This make the game not suited for achieving highest rewards (with high risk) but optimal reward expectation.

### Optimal Policy

Optimal policy $\pi$ guides how the agent acts in its current state.
What is optimal needs to be defined. Maximize expected "discounted future reward sum" (return) is an objective for getting optimal policy.

### Core Challenges of RL

1. Temporal credit assignment 
A sequence of actions led to success/failure: which action(s) to attribute the consequence to?

2. Exploration 
How to take actions to collect a dataset that provides a comprehensive description of the environment?

3. Generalization
How to deal with (very) large state spaces?

### A Machine Learning view of RL

contextual bandits take into account specific user or environment characteristics (context) when choosing an action.
bandits focus on immediate rewards in a single-step scenario.

### A few misconceptions about RL

RL: Planning or Learning??

Two types of scenarios in RL research: 1. Solving a large planning problem using a learning approach (e.g., alphago). Transition dynamics (Go rules) known, but too many states. Run the simulator to collect data. Get good value funtions.
2. Solving a learning problem (e.g.,  adaptive medical treatment). Transition dynamics unknown (and too many states). Interact with the environment to collect data. Great potential for RL, but not realized yet!

Is RL the magical blackbox in machine learning?

1. Contextual bandit is an intermediate framework between SL & RL.
2. General rule: more flexibility/generality = less tractability!
3. So, RL should be your last resort when the problem cannot be handled by any simpler framework.
4. Be cautious about reducing an SL problem to RL—some are legit but many fall into the trap of reducing a simple problem to a more difficult one

## C2: Markov Decision Processes


An MDP $M = (A, S, P, R, \gamma) $

If there is only one action, MDP collaps into Markov Chain with a reward function
If the transition is deterministic, the MDP becomes a directed graph

### Why discounting? (cont.)

Even very light discount make the expected reward finite.
Heavy discount encourages fast planning / learning.

Return: $G_t = \sum_i^N \gamma^k R_{t+1+i}$. A trajectory corresponds with a return. With policy distribution, we can get expected return (value function).
With return we can have state-value function $E_{pi}[G_t|S_t=s]$, action-value or q-value function $E[G_t|S_t=s, A_t=a]$

Adavantage function: difference between state-value and action-value
$E_{\pi}[G_t|A_t=a, S_t=s] - E_{\pi}[G_t|S_t=s]$

Bellman Equation provides recursive formula for calculating value function. Because reward is unrelated to previous states. The recursive equation has a direct solution. $V_{\pi} = R_s + \gamma \sum P_{s}V_{\pi}$

To solve optimal value function, if we know reward and transition probability function, we can solve it via DP, if not, there is no close form solution. We can use Monte-Carlo methods, Temporal difference learning (model-free and learns with episodes), Policy gradient (REINFORCE, Actor-Critic, A2C/A3C, ACKTR, PPO, DPG, DDPG).

Model-free means we don't know transition probability.

Q: again, will using expectation cause an expected best (smooth) but not best policy?

Q: similar to the advantage function that consider a factor (action), can we consider other factors such time, so we get difference between state-value functions from the same state but different time or action-value functions of it.

Q: the problem and its mathematical definition have a lot of assumptions... why can't we design in another way?

