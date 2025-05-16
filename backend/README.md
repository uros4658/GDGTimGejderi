## data

vessels

- size
- type (container, tanker, passanger)
- Draft (depth of the vessel below the waterline)
- eta
- etd

berths

- location
- depth
- equipment

## simulator.py

needs to take in data and berth plan and simulate how it might play out

ex.
1 vessel with eta 0830, 1 with eta 0900, berth plan that says to dock first vessel on 1 at 0840-0910 and second at 0910-0950
simulate with environmental conditions (e.g. bad weather -> vessel arrives at 0910, docks)

