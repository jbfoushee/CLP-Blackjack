from turtle import back, st
import pandas as pd
import numpy as np
import os
import platform

from colorama import init, Fore, Back, Style
init()
# all available foreground colors
FORES = [ Fore.BLACK, Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE ]
# all available background colors
BACKS = [ Back.BLACK, Back.RED, Back.GREEN, Back.YELLOW, Back.BLUE, Back.MAGENTA, Back.CYAN, Back.WHITE ]
# brightness values
BRIGHTNESS = [ Style.DIM, Style.NORMAL, Style.BRIGHT ]

class Color:
    def __init__(self, fore, back, brightness):
        self.fore = fore
        self.back = back
        self.brightness = brightness

# ---------------------------------------------------------------------------
# Project Requirement: Category 1: Create and call at least 3 functions/methods; one returning an object
# ---------------------------------------------------------------------------

def GetInputData():
    # ---------------------------------------------------------------------------
    # Project Requirement: Category 2: Read data from an external file
    # --------------------------------------------------------------------------

    filepath = LocateInputFile()
    df_infile = pd.read_csv(filepath, header=0, sep=',', usecols=["card1", "card2", "ply2cardsum", "card3", "dealcard1", "winloss"])

    print ("Loading data...")

    #Reorder the columns so I can read the data in a logical progression
    df_infile = df_infile[["card1", "card2", "ply2cardsum", "card3", "dealcard1", "winloss"]]

    #----------------------------
    # build computed columns
    #----------------------------
    
    # In a new column, boost all Players' Card1 to 11 if 1
    df_infile.insert(2,"Card1_TrueValue",1)
    df_infile["Card1_TrueValue"] = np.where(df_infile['card1'] == 1, 11, df_infile['card1'])

    # In a new column, boost all Players' Card2 to 11 if 1
    df_infile.insert(3,"Card2_TrueValue",1)
    df_infile["Card2_TrueValue"] = np.where(df_infile['card2'] == 1, 11, df_infile['card2'])

    # In a new column, create a Player's "Max" initial card
    df_infile.insert(4, "MaxCard_TrueValue",1)
    df_infile["MaxCard_TrueValue"] = np.where(
                                        df_infile['Card1_TrueValue'] >= df_infile["Card2_TrueValue"]
                                        , df_infile['Card1_TrueValue']
                                        , df_infile["Card2_TrueValue"])

    # In a new column, create a Player's "Min" initial card
    df_infile.insert(5, "MinCard_TrueValue",1)
    df_infile["MinCard_TrueValue"] = np.where(
                                        df_infile['Card1_TrueValue'] <= df_infile["Card2_TrueValue"]
                                        , df_infile['Card1_TrueValue']
                                        , df_infile["Card2_TrueValue"])

    # Delete the original boosted values because I don't care which order they were dealt
    del df_infile["Card1_TrueValue"]
    del df_infile["Card2_TrueValue"]

    # In a new column, convert the Player's "Max" initial card to "A" if 11
    df_infile.insert(3, "MaxCard_Symbolic",1)
    df_infile["MaxCard_Symbolic"] = np.where(df_infile['MaxCard_TrueValue'] == 11, "A", df_infile['MaxCard_TrueValue'])

    # In a new column, convert the Player's "Min" initial card to "A" if 11
    df_infile.insert(5, "MinCard_Symbolic",1)
    df_infile["MinCard_Symbolic"] = np.where(df_infile['MinCard_TrueValue'] == 11, "A", df_infile['MinCard_TrueValue'])

    # In a new column, generate the Player's initial action based on the value of the 'third' card
    df_infile.insert(8,"Player_Action",1)
    df_infile["Player_Action"] = np.where(df_infile['card3'] > 0, 'Hit', 'Stay')


    # Delete the original player cards
    del df_infile["card1"]
    del df_infile["card2"]
    del df_infile["card3"]

    # In a new column, boost the Dealer's initial card to 11 if 1
    df_infile.insert(7,"Dealcard_TrueValue",1)
    df_infile["Dealcard_TrueValue"] = np.where(df_infile['dealcard1'] == 1, 11, df_infile['dealcard1'])

    # In a new column, convert the Dealer's initial card to "A" if 11
    df_infile.insert(8, "Dealcard_Symbolic",1)
    df_infile["Dealcard_Symbolic"] = np.where(df_infile['Dealcard_TrueValue'] == 11, "A", df_infile['Dealcard_TrueValue'])

    del df_infile["Dealcard_TrueValue"]

    # Treat a Push as a Win, because no money is lost by player
    df_infile["winloss"] = np.where(
                                        df_infile['winloss'] == "Push"
                                        , "Win"
                                        , df_infile['winloss'])

    return df_infile


def LocateInputFile():
    print ("Looking for data...")

    filepath = os.getcwd() + r"\blkjckhands.csv"
    while os.path.exists(filepath) == False:
        filepath = input("Input file not found. Where is it?\n")
    return filepath

def GetUniqueCards():
    data = { 'card': ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'A'] }

    result = pd.DataFrame(data)

    return result

def GetAceCombos():
    result = GetUniqueCards()
    result = result.rename(columns={"card":"MinCard_Symbolic"})

    # In a new column, set a static 'Ace' value
    result.insert(0,"MaxCard_Symbolic",1)
    result["MaxCard_Symbolic"] = 'A'

    # In a new column, combine the two values into a readable format
    result.insert(2,"Display",1)
    result["Display"] = result["MaxCard_Symbolic"] + '/' + result["MinCard_Symbolic"]

    return result

def print_with_color(s, color=Fore.WHITE, brightness=Style.NORMAL, **kwargs):
    #Utility function wrapping the regular `print()` function but with colors and brightness
    print(f"{brightness}{color}{s}{Style.RESET_ALL}", **kwargs, end=' ')

def DemoColorama():
    for fore in FORES:
        for back in BACKS:
            for brightness in BRIGHTNESS:
                print_with_color("A", color=back+fore, brightness=brightness)
        print()

def ColorText(text, confidence):
    color = Fore.WHITE
    brightness = Style.NORMAL
    if confidence < 25.0:
        color = Fore.BLACK + Back.RED
        brightness = Style.DIM
    elif confidence < 40.0:
        color = Fore.RED
        if platform.system() == "Windows":
            brightness = Style.DIM      #show as crimson in Windows
        else:
            brightness = Style.BRIGHT   #show as bright-red in non-Windows
    elif confidence < 48.0:
        color = Fore.RED
        if platform.system() == "Windows":
            brightness = Style.BRIGHT   #show as pink in Windows
        else:
            brightness = Style.DIM      #show as crimson in non-Windows
    elif ((confidence > 48.0) & (confidence < 52.0)):
        color = Fore.YELLOW
        brightness = Style.NORMAL
    elif confidence > 70.0:
        color = Fore.BLACK + Back.GREEN
        brightness = Style.NORMAL
    elif confidence > 52.0:
        color = Fore.GREEN
        brightness = Style.NORMAL          
    else:
        color = Fore.WHITE

    print_with_color(text, color, brightness)

def PrintLegend():
    print("")
    print(" " * 45, end="")
    print("Confidence:")
    print(" " * 30, end="")
    print_with_color("Best", Fore.BLACK + Back.GREEN, Style.NORMAL)
    print(" ", end="")
    print_with_color("Good", Fore.GREEN, Style.NORMAL)
    print(" ", end="")
    print_with_color("Neutral", Fore.YELLOW, Style.NORMAL)
    print(" ", end="")

    brightness = Style.BRIGHT
    if platform.system() == "Windows":
        brightness = Style.BRIGHT   #show as pink in Windows
    else:
        brightness = Style.DIM      #show as crimson in non-Windows

    print_with_color("Bad", Fore.RED, brightness)
    print(" ", end="")

    if platform.system() == "Windows":
        brightness = Style.DIM      #show as crimson in Windows
    else:
        brightness = Style.BRIGHT   #show as bright-red in non-Windows

    print_with_color("Worse", Fore.RED, brightness)    
    print(" ", end="")
    
    print_with_color("Worst", Fore.BLACK + Back.RED, Style.NORMAL)
    print("")


def main():

    df_infile = GetInputData()

    data = { "Display": [*range(8,18)] }
    df_cardsum_results = pd.DataFrame(data)
    #print(df_cardsum_results)

    df_aceCombos = GetAceCombos()
    df_aceCombos_results = pd.DataFrame(df_aceCombos["Display"])
    #print(df_aceCombos_results)


    # Master loop - cycle through dealer's face-up card
    for index, row in GetUniqueCards().iterrows():
        dealer_faceup = row["card"]

        #Limit the dataframe to rows to the dealer's face-up card
        df = df_infile[df_infile['Dealcard_Symbolic'] == dealer_faceup]


        # Filter out players' hands with aces...
        df_noaces = df[df['MaxCard_Symbolic'] != "A"]

        outcomes = []
        for plycardsum in range(8, 18):
            
            dfn = df_noaces[df_noaces['ply2cardsum'] == plycardsum]

            for action in ["Stay", "Hit"]:
                dfny = dfn[dfn['Player_Action'] == action]
                action_count = dfny.shape[0]

                if action_count == 0:
                    continue

                for outcome in ["Win"]:
                    dfnyz = dfny[dfny['winloss'] == outcome]

                    outcome_count = dfnyz.shape[0]
                    outcome_percent = round(int(outcome_count) / int(action_count) * 100,2)
                    outcomes.append([action, outcome_percent, outcome_count, action_count])

        # Add a new column labeled with the dealer face-up card
        df_cardsum_results[dealer_faceup] = outcomes
        outcomes.clear()
        

        # Process players' hands exclusively containing aces
        df_aces = df[df['MaxCard_Symbolic'] == "A"]

        for index, row in df_aceCombos.iterrows():

            dfn = df_aces[df_aces['MaxCard_Symbolic'] == row['MaxCard_Symbolic']]
            dfn = df_aces[df_aces['MinCard_Symbolic'] == row['MinCard_Symbolic']]

            for action in ["Stay", "Hit"]:
                dfny = dfn[dfn['Player_Action'] == action]
                action_count = dfny.shape[0]

                if action_count == 0:
                    continue

                for outcome in ["Win"]:
                    dfnyz = dfny[dfny['winloss'] == outcome]

                    outcome_count = dfnyz.shape[0]
                    outcome_percent = round(int(outcome_count) / int(action_count) * 100,2)
                    outcomes.append([action, outcome_percent, outcome_count, action_count])

        # Add a new column labeled with the dealer face-up card
        df_aceCombos_results[dealer_faceup] = outcomes
        outcomes.clear()


    # End Master loop - cycle through dealer's face-up card

    #print(df_cardsum_results)
    #print(df_aceCombos_results)

    # ---------------------------------------------------------------------------
    # Project Requirement: Stretch: Use pandas, ingest 2 pieces of data, display to a new graph
    # --------------------------------------------------------------------------
    df_temp = pd.concat([df_cardsum_results, df_aceCombos_results], axis=0)
    df_finaldata = df_temp.rename(columns={'Display': 'My Hand'})
    #print(df_finaldata)

    # ---------------------------------------------------------------------------
    # Project Requirement: Category 3: Display data in a tabular form
    # ---------------------------------------------------------------------------

    print((" " * 40) + "Dealer's Face-up card")
    print("My Hand\t\t", end = "")

    for column in df_finaldata.iloc[: , range(1,df_finaldata.shape[1])]:
        print(column + "\t", end = "")
    print("")

    for index, row in df_finaldata.iterrows():
        print(str(row["My Hand"]) + "\t\t", end = "") # no color here

        for columnname in [2,3,4,5,6,7,8,9,10]:
            ColorText(row[columnname][0], row[columnname][1])
            print("\t", end="")
        ColorText(row["A"][0], row["A"][1])
        print_with_color("", Fore.RESET + Back.RESET, Style.RESET_ALL) # reset trailing backcolors? (Windows only)
        print("")

    PrintLegend()
        
main()