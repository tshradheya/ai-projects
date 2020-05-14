# Pacman using QLearning

Main changes in:

- qlearningAgents.py
- featureExtractors.py

## Task 1

- Implement SARS

```
python pacman.py -p PacmanQAgent -x 2000 -n 2010 -l smallGrid

Reinforcement Learning Status:
        Completed 2000 out of 2000 training episodes
        Average Rewards over all training: -76.56
        Average Rewards for last 100 episodes: 216.66
        Episode took 4.33 seconds

Average Score: 500.6
Scores:        499.0, 503.0, 503.0, 503.0, 495.0, 503.0, 503.0, 499.0, 495.0, 503.0
Win Rate:      10/10 (1.00)
Record:        Win, Win, Win, Win, Win, Win, Win, Win, Win, Win
```



```
python autograder.py -q q1

Average Score: 420.12
Scores:        499.0, 503.0, 503.0, 503.0, 495.0, 503.0, 503.0, 499.0, 495.0, 503.0, 495.0, 495.0, 503.0, 503.0, 499.0, 499.0, 499.0, 495.0, 503.0, 499.0, 499.0, 499.0, 499.0, 503.0, 503.0, 495.0, 499.0, 499.0, 503.0, 499.0, 499.0, 499.0, 495.0, 503.0, 499.0, -503.0, 499.0, 499.0, 503.0, 503.0, 499.0, 503.0, 503.0, 499.0, 499.0, 503.0, 499.0, 499.0, 503.0, 503.0, 503.0, 499.0, 503.0, 503.0, 503.0, 503.0, -510.0, 503.0, 503.0, 503.0, 503.0, 495.0, 499.0, 495.0, 495.0, 503.0, -503.0, 499.0, 503.0, 503.0, 499.0, 499.0, -504.0, 503.0, 503.0, 503.0, 499.0, 503.0, -503.0, 495.0, 503.0, 499.0, 503.0, -503.0, 503.0, -503.0, 499.0, 503.0, 503.0, 503.0, -503.0, 503.0, 503.0, 495.0, 499.0, 503.0, 503.0, 495.0, 503.0, 499.0
Win Rate:      92/100 (0.92)


Average Score: -128.34
Scores:        491.0, -509.0, -502.0, 499.0, 491.0, -517.0, -505.0, 491.0, 491.0, 499.0, -511.0, -504.0, 491.0, 491.0, -504.0, -514.0, -504.0, -504.0, -511.0, 491.0, 491.0, -514.0, 491.0, -503.0, -518.0, -517.0, 499.0, 499.0, 491.0, -518.0, 491.0, 491.0, -502.0, -501.0, -519.0, 491.0, 499.0, -517.0, -504.0, 499.0, 491.0, -504.0, 491.0, -506.0, -510.0, 491.0, 499.0, 491.0, -503.0, -510.0, -509.0, 491.0, -505.0, -514.0, 491.0, -512.0, -514.0, -517.0, 491.0, -517.0, -501.0, 491.0, 491.0, -516.0, -512.0, -503.0, -507.0, 491.0, -503.0, -504.0, -509.0, -510.0, -500.0, 491.0, -503.0, -502.0, 499.0, -514.0, -513.0, -511.0, 499.0, -515.0, -513.0, -518.0, 491.0, -510.0, -502.0, -502.0, -510.0, -503.0, 491.0, -502.0, -517.0, 491.0, 491.0, -514.0, 491.0, -503.0, -516.0, -512.0
Win Rate:      38/100 (0.38)


Average Score: 114.6
Scores:        503.0, 495.0, 503.0, 499.0, -508.0, 501.0, -513.0, -513.0, 499.0, -523.0, 501.0, 499.0, 499.0, 503.0, 499.0, 503.0, 499.0, -513.0, 495.0, 503.0, 503.0, -510.0, -513.0, -513.0, -510.0, -510.0, 499.0, 503.0, -515.0, -507.0, -507.0, -507.0, 503.0, 495.0, 503.0, -518.0, -514.0, 499.0, 499.0, 503.0, -523.0, 495.0, 495.0, -510.0, 499.0, 495.0, 503.0, 503.0, 495.0, 500.0, -507.0, -513.0, -515.0, 495.0, -510.0, 500.0, -515.0, 503.0, -513.0, 503.0, -530.0, -513.0, 503.0, -510.0, 495.0, -513.0, 503.0, -505.0, -513.0, 495.0, 499.0, -521.0, -508.0, 495.0, 503.0, 494.0, -507.0, 503.0, 495.0, 499.0, 499.0, 495.0, 499.0, 499.0, -536.0, 501.0, -514.0, 499.0, 499.0, -510.0, 495.0, 495.0, 501.0, 503.0, -520.0, 503.0, 501.0, 503.0, -513.0, 503.0
Win Rate:      62/100 (0.62)
```



## Task 2

- Implement Approximate Qlearning using Features

```
python2 pacman.py -p ApproximateQAgent -a extractor=SimpleExtractor -x 50 -n 60 -l mediumGrid
Weights {'eats-food': 400.75595860131756, 'closest-food': -1.6327102945368759, 'bias': 403.23251742172403, '#-of-ghosts-1-step-away': -20.590314265853205}
Average Score: 526.8
Scores:        523.0, 529.0, 525.0, 529.0, 525.0, 529.0, 529.0, 529.0, 527.0, 523.0
Win Rate:      10/10 (1.00)



python2 pacman.py -p ApproximateQAgent -a extractor=SimpleExtractor -x 50 -n 60 -l mediumClassic -q -f
Weights {'closest-food': -2.8978004321179385, 'bias': 172.6506550694894, '#-of-ghosts-1-step-away': -160.39008477860523, 'eats-food': 271.72196242892352}
Average Score: 1174.9
Scores:        1344.0, 1342.0, 1316.0, -186.0, 1318.0, 1304.0, 1326.0, 1316.0, 1337.0, 1332.0
Win Rate:      9/10 (0.90)


python autograder.py -q q2                  

Question q2
===========

*** PASS: test_cases/q2/1-tinygrid.test
*** PASS: test_cases/q2/2-tinygrid-noisy.test
*** PASS: test_cases/q2/3-bridge.test
*** PASS: test_cases/q2/4-discountgrid.test
*** PASS: test_cases/q2/5-coord-extractor.test

### Question q2: 3/3 ###
```


## Task 3

- Create New Feature extractor


```
Compare score of 

python2 pacman.py -p ApproximateQAgent -a extractor=SimpleExtractor -x 50 -n 60 -l mediumClassic -q -f

and 

python2 pacman.py -p ApproximateQAgent -a extractor=NewExtractor -x 50 -n 60 -l mediumClassic -q -f


```

```
python pacman.py -p ApproximateQAgent -a extractor=NewExtractor -x 50 -n 60 -l mediumClassic

Add -q -f if you want to runn faster



Order (pri_capsule, pri_sacred_``ghost)

# Exp 1: (1/8, 3) Checking 1 step away unscared ghost
        Weights {'closest-food': -2.3252687238837013, 'closest-scared-ghost': 2.4574925399200693, '#-of-scared-ghosts-1-step-away': 148.5352616099526, '#-of-unscared-ghosts-1-step-away': -278.15754026157725, 'bias': 197.63642911255712, '#-of-ghosts-1-step-away': 0.0, 'closest-capsule': 0.0, 'eats-food': 260.62718603694276}
Average Score: 1439.4
Scores:        1312.0, 1524.0, 1502.0, 1281.0, 1460.0, 1511.0, 1353.0, 1672.0, 1483.0, 1296.0
Win Rate:      10/10 (1.00)



# Exp 2: (1/8, 3) No checking how far scared ghosts are. Also a bug fix
        Weights {'closest-food': -3.3485521293790743, 'closest-scared-ghost': 1.126318605675395, '#-of-unscared-ghosts-1-step-away': -122.74079095288897, 'bias': 234.90645832767305, 'closest-capsule': 0.0, 'eats-food': 301.97496842829247}

Average Score: 1411.8
Scores:        1729.0, 1470.0, 1523.0, 1308.0, 1313.0, 1314.0, 1327.0, 1337.0, 1289.0, 1508.0
Win Rate:      10/10 (1.00)

# Exp 3: (1/8, 2) Checking 1 step away unscared ghost and 
        Weights {'closest-food': -3.3847631591867824, 'closest-scared-ghost': 1.3542430043683629, '#-of-unscared-ghosts-1-step-away': -102.72463242945147, 'bias': 260.04542262633873, '#-of-scared-ghosts-1-step-away': 135.66410759702666, 'closest-capsule': 0.0, 'eats-food': 300.6827736382762}
Average Score: 1694.4
Scores:        1732.0, 1740.0, 1748.0, 1736.0, 1728.0, 1734.0, 1925.0, 1532.0, 1537.0, 1532.0
Win Rate:      10/10 (1.00)

# Exp 3(repeated)
Average Score: 1264.9
Scores:        1914.0, 241.0, 1942.0, 1744.0, 1305.0, 1737.0, 1928.0, -331.0, 1737.0, 432.0
Win Rate:      7/10 (0.70)
[Just a very poor scenario where pacman was stuck in middle for multiple times]


# Exp 4 [ Same as 3 but only go for scared shots with 10 time or less
 Weights {'closest-food': -2.8233106788167137, 'closest-scared-ghost': 1.3788339661289286, '#-of-unscared-ghosts-1-step-away': -210.8072843875598, 'bias': 218.30299968862136, '#-of-scared-ghosts-1-step-away': 166.5616693402978, 'closest-capsule': 0.0, 'eats-food': 321.5879169467875}
Average Score: 1592.6
Scores:        1938.0, 1534.0, 1910.0, 1537.0, 1533.0, 1326.0, 1546.0, 1533.0, 1531.0, 1538.0
Win Rate:      10/10 (1.00)


# Exp 5: Same as 4 but only think about capsules when there are are unscared ghosts[BuG]
Average Score: 1090.2
Scores:        1729.0, 1346.0, 1332.0, -317.0, 1720.0, 1726.0, 222.0, 470.0, 1338.0, 1336.0
Win Rate:      7/10 (0.70)

# Exp 6: All are scared ghosts then think about capsule (1/4, 4)
Weights {'closest-food': -3.7170058482330037, 'closest-scared-ghost': -2.0469058082197433, '#-of-unscared-ghosts-1-step-away': -203.28970311211376, 'bias': 228.9801250893308, '#-of-scared-ghosts-1-step-away': 262.10348491162307, 'closest-capsule': 0.0, 'eats-food': 324.1445085325315}
Note: Gets confused and wastes a bit of time cause it doesnt know whether to eat the food or scared ghost
Average Score: 1711.8
Scores:        1731.0, 2144.0, 1713.0, 1724.0, 1938.0, 2137.0, 1714.0, 1909.0, 1730.0, 378.0
Win Rate:      9/10 (0.90)


# Exp 7: Prioritise food when both scared ghost and food
Average Score: 1534.1
Scores:        1728.0, 1538.0, 1713.0, 1344.0, 1323.0, 1904.0, 1495.0, 1505.0, 1295.0, 1496.0
Win Rate:      10/10 (1.00)

# Exp 8: changed capsule-distance multiplier to 3.5 (results using tricky classic)
Average Score: 2803.5
Scores:        2862.0, 2534.0, 3046.0, 2459.0, 1423.0, 2640.0, 3084.0, 3261.0, 3666.0, 3060.0
Win Rate:      9/10 (0.90)
Record:        Win, Win, Win, Win, Loss, Win, Win, Win, Win, Win

# Exp 9: Keep track of completion based on the amount of food remaining, and prioritize capsules based on completion (distghost<7, [3.5,2,1]>) (results using tricky classic)
Average Score: 2644.0
Scores:        1458.0, 3156.0, 2880.0, 2523.0, 2645.0, 3237.0, 1876.0, 3069.0, 2288.0, 3308.0
Win Rate:      8/10 (0.80)
Record:        Loss, Win, Win, Win, Win, Win, Loss, Win, Win, Win

# Exp 10 same as Exp 9 (results using medium Classic)
Average Score: 1756.4
Scores:        1304.0, 1500.0, 1725.0, 1897.0, 1921.0, 1945.0, 1717.0, 1923.0, 1709.0, 1923.0
Win Rate:      10/10 (1.00)
Record:        Win, Win, Win, Win, Win, Win, Win, Win, Win, Win
Notes: not chasing scared ghosts actively. Randomly eating capsules (must avoid if game is not near complete)

# Exp 11 Based on completion level, pacman prioritises eating scared ghost later in the game (7, (0.25)0.8, (0.5)3.5, 8)
Average Score: 1767.1
Scores:        1690.0, 1879.0, 1915.0, 1694.0, 1913.0, 1492.0, 1735.0, 1922.0, 1718.0, 1713.0
Win Rate:      10/10 (1.00)
Record:        Win, Win, Win, Win, Win, Win, Win, Win, Win, Win

Current Master:
Average Score: 1796.0
Scores:        1722.0, 1902.0, 1526.0, 1722.0, 2110.0, 2117.0, 1723.0, 1693.0, 1717.0, 1728.0
Win Rate:      10/10 (1.00)

```