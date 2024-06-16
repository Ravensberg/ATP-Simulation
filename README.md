# ATP-Simulation
Python tool to simulate tennis matches, tournaments and seasons based on real-life ATP data and statistics.

The simulation is based on the 2019 ATP season. All players that played at least 5 games on Clay, Hard or Grass are kept in the database (around 1,0000). Each players has the following stats that are used in a match simulation:
- Ace: as a % of serves
- 1st serve in %: as a % of serves
- 1st serve point won %: as a % of 1st serves
- 2nd serve point won %: as a % of 2nd serves
- break point saved %: as a % of break point faced
- 1st serve return won %: as a % of 1st serves as a returner
- 2nd serve return won %: as a % of 2nd serves as a returner
- break point won %: as a % of break point opportunities

The calendar used is the 2019 season, including all ATP-level and Challenger-level events. The ATP Finals and Davis Cup are excluded. Only singles are in the scope of the simulation. Tie-breaks are included in the simulation, but not Super Tie Breaks. Matches can go on until a player has a 2-game advantage in the last set.

To simulate a match, two players are needed as well as a surface (Hard, Clay or Grass). The simulation structure is as follows:
  > Sets are simulated until one player reaches the required set amount to win: best-of-3 or best-of-5 for Grand Slams
    > Games are simulated until one player reaches the required games amount to win: 6 or 7 if there's a tie, with a 2-game advantage needed in the final set
      > Points are simulated until one player reaches the required points amount to win: 0, 15, 30, 40, GAME with a 2-point advantage needed in the case of a deuce

Points are simulated according to the following logic:
- All stats are %-based and turned to a D1000 roll. If the roll is equal or below the stats, then it's a success.
> The server will roll for his 1st serve
  > If it's in, the server rolls for an Ace
    > If it'a an Ace, the server wins the point
    > If it's not an Ace, the server/returner matchup will determine who wins the point on the 1st serve
  > If the 1st serve is failed, the server rolls for a double fault
    > If it'a a double fault, the returner wins the point
    > If it's not a double fault, the server/returner matchup will determine who wins the point on the 2nd serve

The Server/Returner matchup uses the Log5 formula to determine the probability of an event, based on the probability of an event for the Server and the probability of an event for the Returner. For example, on a 1st serve matchup, the log5 formula will determine the probability that the server wins the point given:
- the Server's 1st serve point won %
- the Returner's 1st serve return won %

This approach may be flawed and matches between evenly matched players tend to be very close and often go to 3/5 sets. 
