import random
from multiprocessing import Pool, cpu_count

"""
# The Gambler Fallacy Simulator 

I wrote this code in response to a moron claiming the Gambler Fallacy over the moon missions.

One version of this ridiculous argument (https://share.google/aimode/z5zvOGaO3obXcbmFr) goes
like this:

The probability of dying in each mission is high, and there had been 5 successful missions, so
there was a high likelihood of dying at the 6th, since no failure had happened previously, so 
nobody would be crazy enough to attempt it.

This is utterly stupid and ignorant, for various reasons.

Considering the maths only, if you assume all the missions (events) are independent, then the 
probability of dying at the 6th mission is exactly the same as all the others, regardless of 
what happened before.

Many people who are illiterate in probability theory and statistics don't understand this, 
and they confuse the law of large numbers with what happens in the single events: the latter
stay independent on each other, past events don't influence the next one and the next one
won't influence future events. They all influence the posterior distribution of the relative 
frequencies of the outcomes, which converge to the theoretical probabilities as the number 
of trials increases, and not vice versa.

This confusion is known as the Gambler Fallacy, and here we explore it, while ignoring what
follows.

We ignore the fact that the assumption that the event independence, that is, the independence 
of the NASA missions from each other, is grossly unrealistic. In fact, it's very likely that the
risks actually decreased as thousands of engineers and other experts learned from the previous 
missions.

We have also tried to simulate the said scenario with high death probabilities, but it's very 
hard to generate enough valid sequences of missions in this case, so we left the hereby code
with a P(death in last mission) = 0.4.

This figure is still much higher than the actual estimated probability of death in the 
real case, which was 1% (see the link to my chat with Gemini above, it has links to 
sources).

As an additional note, we simulated the scenario in detail, that is, we generated sequences of 
missions, took valid sequences only (ie, those that were successful in all the previous missions
, as the scenario prescribes) and then, for each valid sequence, we generated a last mission with
the usual likelihood of death. Finally, we aggregated the results for all the valid sequences we 
found this way. In other words, we applied the Monte Carlo method.

If you know what we're talking about, you will also note that stressing CPUs like that wouldn't be
necessary at all, for we'd just need to generate a lot single missions and count the failed ones, and 
of course, we know the event independence would lead to the same results. However, I suspect that
if the morons could be convinced so easily, I wouldn't need any of this code, so here you are.

## Results

This is the output of one run. Of course, you can take this file and run the simulation yourself.
If you don't eat programming for breakfast, a quick way to do so is https://www.online-python.com/, 
but beware that with large values of `total_trials`, it will kick you out by timeout.

```bash
$ python3 moon_mission_simulation.py 
Simulation starting, with parameters:
    - Number of missions per trial (ie, sequence length): 2-20
    - Total generated mission sequences for each sequence length: 100000000
    - Theoretical probability of death at each mission: 0.4
    
seq_len=2, estimated probability of death at last mission = 0.40001
seq_len=3, estimated probability of death at last mission = 0.39997
seq_len=4, estimated probability of death at last mission = 0.40005
seq_len=5, estimated probability of death at last mission = 0.40001
seq_len=6, estimated probability of death at last mission = 0.39988
seq_len=7, estimated probability of death at last mission = 0.39986
seq_len=8, estimated probability of death at last mission = 0.40016
seq_len=9, estimated probability of death at last mission = 0.39995
seq_len=10, estimated probability of death at last mission = 0.40036
seq_len=11, estimated probability of death at last mission = 0.40022
seq_len=12, estimated probability of death at last mission = 0.40008
seq_len=13, estimated probability of death at last mission = 0.39919
seq_len=14, estimated probability of death at last mission = 0.39906
seq_len=15, estimated probability of death at last mission = 0.39807
seq_len=16, estimated probability of death at last mission = 0.40136
seq_len=17, estimated probability of death at last mission = 0.39752
seq_len=18, estimated probability of death at last mission = 0.39675
seq_len=19, estimated probability of death at last mission = 0.40765
seq_len=20, estimated probability of death at last mission = <didn't generate enough valid missions>
```

"""

def simulate_missions_batch (n_trials, seq_len, p_d):
    """
    The building block: batch simulator.

    Simulates n_trials sequences of independent missions/events, each 
    mission having p_d probability of death and each sequence having
    seq_len missions.

    Returns

    A pair with the total number of valid mission sequences (ie, those that 
    were successful in at least the first seq_len-1 occurrences) and 
    the total number of failed last missions in each sequence.
    """
    rand = random.random
    valid = 0
    deaths_last = 0

    for _ in range(n_trials):
        for _ in range(seq_len - 1):
            if rand() < p_d:
                # death before the end of the sequence, invalid seq, give up
                break
        else:
            # We land here only when the whole 'for' has run without breaks,
            # that is, all previous missions were successful
            valid += 1
            # Now, what happens with the last mission?
            if rand() < p_d: deaths_last += 1
    
    # Done, here the results for the batch
    return valid, deaths_last


def simulate_all(total_trials=1000, seq_len=6, p_d=0.2):
    """
    The simulator orchestrator

    Uses simulate_missions_batch() to simulate total_trials trials of 
    mission/event sequences.

    Given that we need a high number of trials to find valid missions, 
    we run the whole simulation in parallel.

    Returns

    The relative frequency of deaths occurred in the last mission, for
    all the valid missions (ie, those that were successful before the 
    last one).

    Non-valid missions are discarded, since they have nothing to do with 
    the scenario we are simulating, they're only generated because there
    is no other way to find valid mission to aggregate figures from.

    A result is returned only if we have enough valid sequences, which we 
    set to the reasonable value of at least 10000.
    """
    n_proc = cpu_count() - 1 # parallelism degree
    chunk = total_trials // n_proc
    
    # Let's go parallel
    with Pool(n_proc) as pool:
        results = pool.starmap(
            simulate_missions_batch,
            [(chunk, seq_len, p_d)] * n_proc
        )

    total_valid = sum(v for (v, d) in results)
    total_deaths = sum(d for (v, d) in results)

    # As mentioned above, total_valid is increasingly low as seq_len grows, and results 
    # are non significant when we don't have enough simulated data points
    if total_valid <= min ( 10000, total_trials / 10 ): return -1.0
    return total_deaths / total_valid 

def simulate_seq_size_range ( max_total_seq_len, total_trials = 1000, p_d = 0.2 ):
  """
  The overall runner

  Runs the mission simulator simulate_all() for various sequence lengths and collects
  the results as a function of seq_len

  Returns

  A table of [seq_len, relative freq of death at last mission | previous successes].
  This result is currently not used, but might be useful, eg, to be given to 
  matplotlib and draw a chart.

  """
  print ( 
    f"""Simulation starting, with parameters:
    - Number of missions per trial (ie, sequence length): 2-{max_total_seq_len}
    - Total generated mission sequences for each sequence length: {total_trials:,}
    - Theoretical probability of death at each mission: {p_d}

    """
  )

  seq_lengths = []
  death_freqs = []
    
  for seq_len in range(2, max_total_seq_len + 1):
    deaths = simulate_all ( total_trials=total_trials, seq_len=seq_len, p_d=p_d )
    result_str = ""  
    if deaths >= 0:
      seq_lengths.append(seq_len)
      death_freqs.append(deaths)
      result_str = f"{deaths:.5f}"
    else:
      result_str = "<didn't generate enough valid missions>"
    
    print(f"seq_len={seq_len}, estimated probability of death at last mission = {result_str}")

  return seq_lengths, death_freqs

# Usual Python way to run the file if it's called as a script, and not imported as a module
if __name__ == "__main__":
  seq_lengths, death_freqs = simulate_seq_size_range ( 
     max_total_seq_len = 20, total_trials = 100_000_000, p_d = 0.4 
  )
