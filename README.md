# 🤖 Project: Build-a-Forward-Planning-Agent🧠💥

## Welcome to the Magical World of Classical Search & Planning! 🧠🧙‍♂️

Welcome to the second episode of "How Did I End Up Doing This Again?" In this project, I took a deep dive into the world of **progression search**, **symbolic logic**, and **heuristics** to create a planning agent that could make even the most stubborn airplanes take off! ✈️🛫

The project required implementing various **search algorithms**, running them on **air cargo problems**, and analyzing the results until my brain turned into a planning graph. Buckle up, because this ride is going to be wild! 🚀

---

## Project Introduction 🤓

In this thrilling sequel, I tackled the complex task of combining **symbolic logic** and **classical search** to create an agent that solves planning problems using **progression search**. Essentially, my job was to make sure that when the agent says "Have your cake and eat it too," it knows exactly which search algorithm to use to get there (spoiler: *don’t use Breadth-First Search* 🥲).

### The highlights of this journey include:
- 🧩 Implementing a planning graph with mutex rules (because nothing says "fun" like managing inconsistent effects and interference!).
- 🚀 Experimenting with different search algorithms to understand their performance under different conditions.
- 📊 Creating fancy graphs and tables to analyze all the **suffering** I mean, *data* that I collected!

---

## Solver Functionality 🛠️

| Criteria                               | Submission Requirements                                                                                                                                                  |
|----------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 🧠 Mutexes Implemented Correctly        | **(AUTOGRADED)** My code passes all the Project Assistant test cases for: ActionLayer mutual exclusion rules (`_inconsistent_effects()`, `_interference()`, `_competing_needs()`), and LiteralLayer mutual exclusion rules (`_inconsistent_support()`, `_negation()`). 🛠️  |
| ➕ Heuristic Implementation             | **(AUTOGRADED)** I bravely implemented several heuristics for the planning graph and they *actually* passed the tests: `h_levelsum()`, `h_maxlevel()`, `h_setlevel()`. **Heuristics** — because guessing just wasn’t good enough anymore! 🧐 |

---

## How I Survived the Project (aka The Journey to Mordor) 🧙‍♂️

### Step 1: The Beginning of the End 💻

First things first: before doing anything, I made sure to read **Chapter 10 of Artificial Intelligence: A Modern Approach** (aka the AI Bible 📖). It’s full of planning goodness, search algorithms, and enough technical details to make your head spin! ⚙️

After digesting all that knowledge, I felt like Neo from *The Matrix* — ready to dodge planning problems left and right. But spoiler alert: reality is always harder. 🥲

---

### Step 2: Setting Up the Environment 🏗️

Whether you want to battle it out in Udacity’s **Workspace** or fight the code locally with **Pypy3**, the setup is crucial. Here's how I set up my environment to ensure my planning agent could run without blowing up my computer. 💥

#### **Local Setup**:

1. I activated the **aind** conda environment:
   ```bash
   $ source activate aind
   ```

2. Downloaded **Pypy3** for super-speedy performance (you know, because we’re racing the clock here ⏰):
   ```bash
   $ pypy3 example_have_cake.py
   ```

3. Ran the **example problem** script:
   ```bash
   $ python example_have_cake.py
   ```

4. If everything worked (and I didn’t break my laptop), it printed out the problem domain and solved it with different algorithms.

---

### Step 3: Implementing the Planning Graph (aka Brain Fry Time) 🧩🧠

This is where the real magic happens. My job was to implement mutex rules to make sure actions didn’t accidentally interfere with each other — because we can’t have airplanes taking off without any runways! ✈️

#### Key Mutex Rules I Handled:
- **Inconsistent Effects**: Two actions that undo each other can’t happen at the same time. Duh. 🤯
- **Interference**: When one action messes up the preconditions for another. 💥
- **Competing Needs**: Two actions that need mutually exclusive actions themselves. *It's like trying to make coffee while the kettle’s on strike!* 😱

```python
def _inconsistent_effects(self, actionA, actionB):
    """ The effects of one action must not undo the effects of the other """
    return bool(set(actionA.effect_add) & set(actionB.effect_rem))

def _interference(self, actionA, actionB):
    """ The precondition of one action must not contradict the effects of the other """
    return bool(set(actionA.precond_pos) & set(actionB.effect_rem))

def _competing_needs(self, actionA, actionB):
    """ The precondition of one action must not be mutex with the precondition of the other """
    return bool(set(actionA.precond_neg) & set(actionB.precond_pos))
```

---

### Step 4: Heuristic Implementation 🧮📈

Once the planning graph was up and running, I realized that I wasn’t done. Oh no, now I had to add **heuristics**. It turns out, guessing which path to take can be improved with a little help from some well-placed logic! 🧙‍♂️

Here are the heuristics I implemented:

- **h_levelsum()**: The sum of levels at which each goal appears. This one was a beast but gave me some decent results!
- **h_maxlevel()**: The maximum level at which any goal first appears.
- **h_setlevel()**: The first level where all goals appear without any mutex conflicts.

```python
def h_levelsum(self):
    """Calculate the levelsum heuristic for the planning graph"""
    return sum(self.literal_layers[level].get(goal, float('inf')) for goal in self.goal)

def h_maxlevel(self):
    """Calculate the max level heuristic"""
    return max(self.literal_layers[level].get(goal, 0) for goal in self.goal)

def h_setlevel(self):
    """Calculate the set level heuristic"""
    level = 0
    while not self._is_leveled:
        last_layer = self.literal_layers[-1]
        if all(goal in last_layer for goal in self.goal):
            return level
        self._extend()
        level += 1
    return -1
```

---

### Step 5: Experiments & Results 📊🎯

After implementing everything, it was time to **run experiments**. This part was *so much fun* (said no one ever 😅). I tested a variety of **search algorithms** on **air cargo problems** to see how they performed.

Here’s what I ran:
1. Breadth-First Search (aka "Why Is This So Slow?") 🐢
2. Uniform Cost Search (because optimality matters sometimes!) 🧠
3. Greedy Best-First Search (Fast, but *chaotic*.) 🚀
4. A* Search (The overachiever of algorithms!) ✨

Each time I ran the algorithms, I recorded:
- **Number of nodes expanded** 🌳
- **Time to complete the search** ⏳
- **Length of the plan returned** 🛣️

---

### Step 6: Graphing My Sanity 📈📉

After collecting all that glorious data, I plotted some **graphs** and **tables** to make sense of it all (because who doesn’t love staring at charts for hours? 📊).

#### Key Insights:
- **Breadth-First Search** was slower than a snail on a treadmill. 🐌
- **A* Search** is *king* when it comes to balancing speed and optimality. 👑
- Greedy algorithms are fast but unpredictable — like a cat chasing a laser pointer. 🐱💥

---

## Project Submission Instructions 📤

Here’s how you can submit your own project (and avoid hours of frustration like me):

1. Make sure your `my_planning_graph.py` file passes all the **autograder tests**.
2. Write up your **report.pdf** with all the juicy details about your experiments (charts, tables, and deep insights — the whole nine yards).
3. Submit using **Udacity’s submission script**:
   ```bash
   $ udacity submit
   ```

---

## Reviewer’s Note ✨

### 🎉 **Success!** 🎉

A special note from my awesome Udacity reviewer:

> **Fantastic work buddy, you've successfully passed!** 😎👏 However, there’s always room for improvements, and I recommend a couple of things:
>
> - Check out the PEP8 style guide to improve your Python syntax! 🐍✨ [PEP8 Style Guide](https://www.python.org/dev/peps/pep-0008/)
> - Consider optimizing the following code:
>
> ```python
> def h_maxlevel(self):
>     """ Calculate the max level heuristic for the planning graph
>     The max level is the largest level cost of any single goal fluent.
>     The "level cost" to achieve any single goal literal is the level at
>     which the literal first appears in the planning graph. Note that
>     the level cost is **NOT** the minimum number of actions to achieve
>     a single goal literal.
>     For example, if Goal1 first appears in level 1 of the graph and
>     Goal2 first appears in level 3, then the levelsum is max(1, 3) = 3.
>     Hint: expand the graph one level at a time until all goals are met.
>     See Also
>     --------
>     Russell-Norvig 10.3.1 (3rd Edition)
>     Notes
>     -----
>     WARNING: you should expect long runtimes using this heuristic with A*
>     """
>     self.fill()
>     level_cost = 0
>     for goal in self.goal:
>         for cost, layer in enumerate(self.literal_layers):
>             if goal in layer:
>                 level_cost = max(cost, level_cost)
>                 break
>     return level_cost
> 
> def h_setlevel(self):
>     """ Calculate the set level heuristic for the planning graph
>     The set level of a planning graph is the first level where all goals
>     appear such that no pair of goal literals are mutex in the last
>     layer of the planning graph.
>     Hint: expand the graph one level at a time until you find the set level
>     See Also
>     --------
>     Russell-Norvig 10.3.1 (3rd Edition)
>     Notes
>     -----
>     WARNING: you should expect long runtimes using this heuristic on complex problems
>     """
>     def AllGoalSeen(layer):
>         for goal in self.goal:
>             if goal not in layer:
>                 return False
>         return True
>         
>     def NoMutex(layer):
>         for goal1, goal2 in combinations(self.goal, 2):
>             if layer.is_mutex(goal1, goal2):
>                 return False
>         return True
>         
>     level = 0
>     while not self._is_leveled:
>         last_layer = self.literal_layers[-1]
>         if AllGoalSeen(last_layer) and NoMutex(last_layer):
>             return level
>         self._extend()
>         level += 1
>         
>     return -1
> ```
> **WARNING**: You’ll need a lot of patience using these heuristics on complex problems – but I promise, it’s worth it!

## How to Run This Masterpiece 💎

Want to feel like a planning genius? Here’s how:

1. **Clone the repo**:
   ```bash
   git clone https://github.com/pranav8991/Build-a-Forward-Planning-Agent.git
   ```

2. **Activate the environment**:
   ```bash
   conda activate aind
   ```

3. **Run the cake problem** (because you always need cake 🍰):
   ```bash
   python example_have_cake.py
   ```

4. **Unleash the search algorithms**:
   ```bash
   python run_search.py -m
   ```

---

## Conclusion 🍰

This project was a wild ride from start to finish. 🏁 I’ve learned more about **planning graphs**, **mutexes**, and **heuristics** than I ever wanted to, and I’ve got the charts to prove it! 😅 If you ever need help planning a multi-airplane cargo mission (or solving a cake-related crisis), I’m your person. 🎂

##Just remember — even the mightiest programmers start with baby steps (and occasional tantrums). And hey, sometimes those baby steps mean seeking help from fellow coders, dissecting their code, and piecing together solutions. So yes, I’ve had my fair share of peeking into others' projects, learning from their work, and figuring out how things tick. It’s all part of the journey. So, maff kar do muja if I borrowed an idea or two along the way—because, in the end, it’s about growing and improving. 😅

---

## License ⚖️

This project is licensed under the "I Need a Break After This" License. Feel free to fork, share, or modify — but be sure to leave a note if you discover an even better heuristic! 😄

---
