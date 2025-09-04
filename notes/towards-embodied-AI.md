# Toward Embodied AGI: A Review of Embodied AI and the Road Ahead - Reading Notes

## About the Paper

**Paper:** [Toward Embodied AGI: A Review of Embodied AI and the Road Ahead](https://arxiv.org/abs/2505.14235) <br>

**Authors:** Yequan Wang, Aixin Sun  <br>

**DOI:** https://doi.org/10.48550/arXiv.2505.14235  <br>


## Definition

Embodied AGI is a form of Embodied AI that demonstrates human-like interaction capabilities and can successfully perform diverse, open-ended real-world tasks at a human-level proficiency.
*(I am not sure if human-level proficiency is necessary in the definition)*

## L1-L5 Objectives

The authors define 5 levels of objectives in the roadmap of embodied AI. For each level, there are detailed requirements from six aspects: modalities, humanoid, real-time, generalization, body&control.

It seems these requirements are not independent. Capabilities for some requirements are prerequisites for others.

L1: single-task completion. No generalization ability on new tasks, not mentioning other advanced capabilities (such as humanoid).

L2: compositional task completion. It refers to the ability of decomposing high-level human instructions into a sequence of simpler actions.
*(It is interesting that the authors define L2 like this. I would like to see more references. Is task decomposition a necessary step from L1 to L3? Doesn't it uniquely exist in L2, so when embodied AI reaches L3, should task decomposition be eliminated?)*

L3: conditional general-purpose task completion. Embodied AI has cross-tasks, cross-environment, and human instruction abilities. This step starts to require real-time responsiveness and full modalities.

L4: highly general-purpose robots. It reaches true general-purpose capability. Accurate and strong decision-making abilities in real-worlds. It starts to require human-like communication and interaction.

L5: All-purpose robots. These robots have deep understanding of physical laws and human emotional and social dynamics.
*(When illustrating the 5 levels, analogies from LLM and automotive driving cases are used. I think these comparisons are not so intuitive. Each level should present the abilities of robot controlling, sensing, reasoning, and learning with examples.)*
*(Timely responsiveness is a too huge leap in AI-based robotics, I would say. It can have multi-levels between L2 to L4. If we use large models to make decisions, real-time responsiveness is a big challenge, as reasoning time takes too long to support tasks requiring instant reaction)*


## L3 ∼ L5: Key Constituents

1. Omnimodal capabilities

2. Humanoid cognitive behaviors

3. Real-time interaction. 
A widely explored solution is developing small models sacrificing the parameter scale. Real-time auditory and visual interactions are commonly implemented using Time Division Multiplexing. 
However, these approaches encounter scalability issues when incorporating additional modalities, as computational complexity increases quadratically with sequence length. 

4. Generalization to open-ended tasks. Unsupervised or multitask pretraining are insufficient in learning the physical world laws, which is inherently a limitation.

## A Conceptual Framework for L3+ Robots

Their framework defines the inputs which are from full modalities, outputs which are action sequences, monologues, and reasoning, and the streaming nature between the inputs and outputs.

As for training paradigm, it could involve multimodal training from scratch, lifelong learning, and physical-oriented training.
*(The conceptual framework is interesting and should be more detailed. Currently it is still not clear how the real-time streaming is possible because the input and output throughput and processing time is very asymmetric, which can make streaming nonsensical)*