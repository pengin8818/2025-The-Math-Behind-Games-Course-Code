class DialogueNode:

    """
    This is a class that stores text, and dialogue options as a node network.
    """

    def __init__(self, title: str, text: str) -> None:
        # this is the title of this dialogue option, for example, "Tell me more about the town."
        self.title = title

        # this assigns this node's text to be the text entered when the class is instantiated
        # example: "This town is really old, and strange things have been occurring lately"
        self.text = text

        # this is the list of dialogue options you unlock by using this node. They start empty and we
        # will need to create a helper method to link nodes together by adding them to this list.
        self.options = []

    def link_options(self, *options) -> None:
        # This appends dialogue options to already created nodes
        #the * indicates that any number of options can be allowed

        for option in options:
            self.options.append(option)

    def __str__(self) -> str:
        # __str__ is the string format builtin method that tells python how to format things when you
        # use the print() function
        return self.text

    def get_title(self) -> str:
        return self.title

    def get_options(self) -> list:
        return self.options


class Character:

    """This is the class we will use for characters that have dialogue"""

    def __init__(self, name: str) -> None:
        self.name = name
        # the dialogue roots are the roots of our dialogue trees. These are the original options you
        # have to speak to a character at the start of the conversation
        self.dialogue_roots = []
        self.current_node = None  # this changes as we pass through their dialogue tree

    def add_roots(self, *dialogue_tree: DialogueNode) -> None:
        for root in dialogue_tree:
            self.dialogue_roots.append(root)

    def show_and_choose(self) -> DialogueNode:
        # shows all current dialogue options and allows you to choose one
        # returns the text associated with the choice you made
        # assigns the
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