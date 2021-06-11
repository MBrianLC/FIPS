# Reimplementation of FIPS 140-2 battery

This is a reimplementation of the FIPS 140-2 battery (https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.140-2.pdf) in Python. It also includes certain modifications over the original battery:

- The tests can be applied to sequences of any size (not just 20,000, as with the original battery).
- For each sequence, each test returns two values: a statistic and a p-value, which give more information about the randomness of the stream (the original battery only indicates if the sequence has passed the test or not).

The Long Run and Continuous Run tests are also slightly different: in the original FIPS, they directly fail the test if a specific requirement is met, while now the test counts the number of times this occurs and obtains a p-value associated with this quantity. Furthermore, both tests depend on a parameter that allows them to have variations (minimum run size in Long Run and block size in Continuous Run).
