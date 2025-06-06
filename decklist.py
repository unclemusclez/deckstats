"""Functions to read in a decklist and assign parameters to the cards it contains"""
from .api_requests import jprint, loadcarddata, getcarddata, downloadcardimage
import os
import json


def make_deck_folder(deckfilename):
    deckfoldername = deckfilename.split('.')[0]
    if not os.path.isdir(deckfoldername):
        os.mkdir(deckfoldername)
        os.mkdir(deckfoldername + '/images')
    return deckfoldername


def parse_decklist_lines(lines):
    maindeck = []
    sideboard = []
    current_section = maindeck

    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.lower().startswith('sideboard'):
            current_section = sideboard
            continue

        try:
            quantity, card_name = line.split(' ', 1)
            quantity = int(quantity.strip())
            card_name = card_name.strip()
            current_section.extend([card_name] * quantity)
        except ValueError:
            print(f"Skipping invalid line: {line}")

    return maindeck, sideboard

def decklist_readin(deckfilename):
    with open(deckfilename) as f:
        lines = f.readlines()

    make_deck_folder(deckfilename)
    maindeck, sideboard = parse_decklist_lines(lines)
    return maindeck, sideboard


def assignparams(deckfilename, cardlist, carddata):
    deckfoldername = make_deck_folder(deckfilename)
    assignedcardlist = []
    for card in cardlist:
        assignedcard = getcarddata(card, carddata)
        assignedcardlist.append(assignedcard)
    if len(assignedcardlist) == 15:
        listtype = 'sideboard'
    else:
        listtype = 'maindeck'
    filename = deckfoldername + '/' + listtype + '.json'
    with open(filename, 'w') as f:
        json.dump(assignedcardlist, f)
    return assignedcardlist


def getdeckimages(deckfilename, cardlist, carddata):
    deckfoldername = make_deck_folder(deckfilename)
    for card in cardlist:
        downloadcardimage(deckfoldername + '/images/', card, carddata)

def run(deckname):
    carddata = loadcarddata()
    maindeck, sideboard = decklist_readin(deckname)
    assignedmaindeck = assignparams(deckname, maindeck, carddata)
    assignedsideboard = assignparams(deckname, sideboard, carddata)
    getdeckimages(deckname, maindeck, carddata)
    getdeckimages(deckname, sideboard, carddata)
    return assignedmaindeck, assignedsideboard

if __name__ == '__main__':
    deckname = 'Deck - Spirits v11.txt'
    maindeck, sideboard = run(deckname)
    # jprint(maindeck)
