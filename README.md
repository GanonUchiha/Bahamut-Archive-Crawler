# Bahamut Board Archive Crawler

A Python program that fetches the content from the Archive section of the discussion boards, on the forum website [Bahamut](https://www.gamer.com.tw/).

## Objective
Given a list of board URLs, look up their Archive section, and output the entire archive as a text file. Since the archives organizes their entries in a hierarchical tree structure, the output should also be able to display the heirarchical structure.

## Usage

1. run `python src/crawler_interactive.py` in your command prompt
1. Enter a URL that leads to the Archive Section of a board, for example: `https://forum.gamer.com.tw/G1.php?bsn=60076`
1. the result should show up in the `output` folder, in both `.txt` and `.csv` format.

## Environment

This program mainly uses the following packages:
| Package | Version |
|---|---|
| python | 3.10.4 |
| requests | 2.28.1 |
| lxml | 4.9.1 |
| bs4 | 4.11.1 |

Detailed packages and versions can be found in `requirements.txt`. To create an identical virtual environment in Anaconda, use the command `conda create --name <env> --file requirements.txt`.
