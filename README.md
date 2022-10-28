Headless-SDK
============

Overview
--------

The ElectrumSV headless SDK is a complete standalone regtest development environment for BitcoinSV.

It features the following components:

* The node.
* The Merchant API server.
* The HeaderSV server.
* The Direct Payment Proxy server.
* ElectrumSV.

Platforms
---------

Builds are released for:

* Linux.
* Windows (64 bit).

We make builds for:

* Linux.
* MacOS.
* Windows (64 bit).

The reason we do not make available our MacOS builds is that it is not possible to run them
as they are not notarised. Apple will make it very hard to run them, if it is even possible,
and it is not currently something we have time to do.

Usage
-----

To start the core components:

```
electrumsv-sdk start node
electrumsv-sdk start merchant_api
electrumsv-sdk start header_sv
```

You can execute JSON-RPC commands against the node to do things like generating a block on demand:

```
electrumsv-sdk node generate 1
```

Sample blockchains
------------------

If you want sample blockchains and wallets to work with, with different types of transactions
present from multi-signature to P2PKH, you can find blockchains you can import and scripts
you can import them with in our
[simple indexer project](https://github.com/electrumsv/simple-indexer/tree/master/contrib).


Example
~~~~~~~

To import a 115 block chain with a mining wallet that you can restore in ElectrumSV with
existing mature and immature coins (immature coins are unspendable due to mining rules),
you can do the following:

```
git clone https://github.com/electrumsv/simple-indexer.git
cd simple-indexer/contrib
python3 scripts/import_blocks.py blockchains/blockchain_115_3677f4
<in another terminal>
electrumsv-sdk node generate 1
```

The reason you need to generate the new block on top of the imported blockchain is that a node
that does not have any recent blocks will be in "initial download mode" and will not behave like
an active node. The new block triggers it to leave that mode and start communicating with
other connected applications fully.
