"""
Your Assignment:

Fill out all the blank methods and functions below! Instructions for each are provided in the green comment text!
"""




class DialogueNode:

    """
    This is a class that stores text, and dialogue options as a node network.
    """

    def __init__(self, title: str, text: str) -> None:

        """
        store each of the following local variables

        title: This variable is the title of this dialogue node. For example "What is your name?" could be the title
        of a dialogue node at the start of a tree when conversing with an NPC

        text: This variable is a string of the text that would be displayed when this option is printed out. For example
        "My name is John Doe and I have a quest for you!"

        options: This is a list variable containing all nodes that branch out from this option. For example, the node
        "What is your name?" could branch out to another node "That's a weird name..."
        """

    def link_options(self, *options) -> None:
        """
        This method adds any number of other DialogueNodes to this DialogueNode's options list. The * in *options
        means that this method can take any number of inputs, so treat the variable 'options' as an
        iterable object like a list

        hint: use a for loop
        """



    def __str__(self) -> str:
        """this is a built-in method that defines what Python does when you put this DialogueNode object into
        the print() function. return the value of this node's text local variable"""

    def get_title(self) -> str:
        """
        Return this node's title local variable
        """

    def get_options(self) -> list:
        """
        Return this node's options local variable
        """


class Character:

    """This is the class we will use for characters that have dialogue"""

    def __init__(self, name: str) -> None:

        """
        name: This is just the text name of this character, and should be assigned to the input variable 'name'

        dialogue_roots: this is a list of DialogueNodes that appear the second you start speaking to a character

        current_node: starts as None, but every time the player selects a new node this will be set to whatever
        DialogueNode they chose. If the DialogueNode has no children (no options), set this back to None.
        """

    def add_roots(self, *dialogue_tree: DialogueNode) -> None:
        """
        This method takes any number of dialogue nodes, and adds them to the Character's own dialogue_roots local
        variable

        Hint: Use for loops to iterate over *dialogue_tree since it can take multiple inputs
        """

    def show_and_choose(self) -> DialogueNode:
        """
        This method is already completed for you since it is kind of complicated
        """
        display_string = ""

        if self.current_node is not None and len(self.current_node.get_options()) == 0:
            self.current_node = None

        i = -1
        if self.current_node is None:

            for option in self.dialogue_roots:
                i += 1
                display_string = display_string + str(i) + ". " + option.get_title() + "\n"
        else:
            for option in self.current_node.get_options():
                i += 1
                display_string = display_string + str(i) + ". " + option.get_title() + "\n"

        choice = int(input("Enter the number of your choice...\n" + display_string))
        if self.current_node is None:

            self.current_node = self.dialogue_roots[choice]

        else:
            self.current_node = self.current_node.get_options()[choice]

        print(self.current_node)
        return self.current_node

"""
Below is some code that should work properly if you set this up correctly. 
"""

A = DialogueNode("Who are you?", "My name is the dialogue testing bot.")
B = DialogueNode("What is going on?", "You are testing the dialogue tree that Tyler created.")
A1 = DialogueNode("Tell me a fun fact!", "It is constantly raining iron dust due to asteroids breaking up in the upper atmosphere.")
A2 = DialogueNode("Are you like ChatGPT?", "No, I am far simpler since my dialogue is pre-programmed.")
B1 = DialogueNode("What is your purpose?", "To test out this branching dialogue system. \nFun fact: You could have gotten to this option by starting from somewhere else in the tree!")
B2 = DialogueNode("Why does it need testing?", "Because Tyler is not that good at programming. Don't tell him I said that.")
C1 = DialogueNode("That fact wasn't very fun...", "I thought it was pretty fun :(")
C2 = DialogueNode("How complex can your dialogue get?", "As complex as you program me to be!")
C3 = DialogueNode("That's interesting, how do you make the branching work like that?", "Tyler assigned the previous dialogue node as the child of two different nodes. \nThat way two choices result in the same option being provided")
C4 = DialogueNode("Why is he allowed to teach this course?", "I don't know honestly.")

A.link_options(A1, A2, B1)
B.link_options(B1, B2)
A1.link_options(C1)
A2.link_options(C2)
B1.link_options(C3)
B2.link_options(C4)


test_robot = Character("Test Robot")

test_robot.add_roots(A)
test_robot.add_roots(B)

while True:
    test_robot.show_and_choose()