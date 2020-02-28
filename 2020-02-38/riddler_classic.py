import random
from typing import List, Optional

import tqdm

def simulate(num_barbers: int = 4,
             haircut_time: int = 15,
             num_other_customers_in_line: int = 1,
             per_chance_wait_tiffany: float = .25,
             initial_wait_times: Optional[List[float]] = None,
             initial_customers_prefer_tiffany: Optional[List[bool]] = None
             ) -> float:

    # Randomly initialize the time remaining for each barber (0 is Tiffany) if
    # not provided
    barbers_current_time_remaining = (initial_wait_times
                                      if initial_wait_times is not None
                                      else [random.randrange(0, haircut_time)
                                            for _ in range(num_barbers)])

    # Randomly determine whether customers prefer tiffany if not provided
    customers_prefer_tiffany = (initial_customers_prefer_tiffany
                                if initial_customers_prefer_tiffany is not None
                                else [random.random() < per_chance_wait_tiffany
                                      for _ in range(num_other_customers_in_line)])

    wait_time = 0

    for customer_id in range(len(customers_prefer_tiffany)):
        if customers_prefer_tiffany[customer_id]:
            # If customer prefers tiffany then just add them to her time
            barbers_current_time_remaining[0] += haircut_time
            continue

        # Allow the barber who is closest to finishing to finish.
        next_barber_i = barbers_current_time_remaining.index(
            min(barbers_current_time_remaining)
        )
        elapsed_time = barbers_current_time_remaining[next_barber_i]
        # Add the time for that barber to finish to the wait time
        wait_time += elapsed_time
        # and subtract it from the rest of the barbers
        barbers_current_time_remaining = [time - elapsed_time
                                          for time in barbers_current_time_remaining]

        # The barber with the least amount of time just got a new client so
        # reset their time remaining
        barbers_current_time_remaining[next_barber_i] = haircut_time

    # All the customers ahead of you are now being served. We're waiting for
    # Tiffany so we should add her remaining time to the wait time
    wait_time += barbers_current_time_remaining[0]

    return wait_time

# 10 min initial wait, plus customer will wait for tiffany so additional 15 min
assert simulate(initial_wait_times=[10, 9],
                initial_customers_prefer_tiffany=[True]) == 25

# 10 min initial, customer will go to barber 2, so total total 10 min wait
assert simulate(initial_wait_times=[10, 9],
                initial_customers_prefer_tiffany=[False]) == 10

# Tiffany finishes first so initial 10 min wait, then she sees customer even
# though no preference
assert simulate(initial_wait_times=[10, 11],
                initial_customers_prefer_tiffany=[False]) == 25

# 10 min initial wait, first customer sees tiffany since shes done first,
# 2nd customer waits on tiffany, total time 40 min
assert simulate(initial_wait_times=[10, 15],
                initial_customers_prefer_tiffany=[False, True]) == 40

assert simulate(initial_wait_times=[10, 15, 10],
                initial_customers_prefer_tiffany=[False, True, False, False]) == 40

ITERATIONS = 100_000_000

results = [simulate() for _ in tqdm.tqdm(range(ITERATIONS))]

print(sum(results) / ITERATIONS)

# Output 13.95017875

