class Node:
    def __init__(self, PId):
        self.PId = PId
        self.left = None
        self.right = None
        self.attrCtr = 1  # Initial attrCtr value when a player enters the hotel

class BioBubble:
    def __init__(self):
        self.root = None

    def insert(self, PId):
        self.root = self._recordSwipeRec(self.root, PId)

    def _recordSwipeRec(self, pNode, PId):
        if not pNode:
            return Node(PId)

        if PId == pNode.PId:
            pNode.attrCtr += 1 #increment the counter variable for each swipe
        elif PId < pNode.PId:
            pNode.left = self._recordSwipeRec(pNode.left, PId)
        else:
            pNode.right = self._recordSwipeRec(pNode.right, PId)

        return pNode
    
    def read_swipes_from_file(self, filename):
        with open(filename, 'r') as input_file:
            for line in input_file:
                player_id = int(line.strip())
                self.insert(player_id)
    
    def _getSwipeRec(self, pNode):
        if pNode is None:
            return 0
        else:
            # Recursively count nodes in the left and right subtrees
            left_count = self._getSwipeRec(pNode.left) if hasattr(pNode, 'left') else 0
            right_count = self._getSwipeRec(pNode.right) if hasattr(pNode, 'right') else 0
            
            # Include the current node in the count
            return 1 + left_count + right_count

    def _getSwipe(self):
        count = self._getSwipeRec(self.root)

        with open('outputPS04.txt', 'a') as output_file:
            output_file.write(f"Total number of players recorded today: {count}\n")

    def _frequentVisitorRec(self, pNode, frequency):
        result_list = [] #creating a empty result list to store the id and its counter value

        def helper(node): #function to traverse through the tree
            nonlocal result_list
            if not node:
                return

            if node.attrCtr >= frequency: #comparing the counter value with input frequency if >= adding the result set
                result_list.append((node.PId, node.attrCtr))

            helper(node.left)
            helper(node.right)

        helper(pNode)

        return result_list

    def frequent_visitor(self, frequency):
        result_list = self._frequentVisitorRec(self.root, frequency)

        with open('outputPS04.txt', 'a') as output_file:
            if result_list:
                output_file.write(f"Players that swiped more than {frequency} times today are: ")
                for player_id, count in result_list:
                    output_file.write(f"Player id {player_id}, count {count}. ")
                output_file.write("\n")
            else:
                output_file.write(f"No players swiped more than {frequency} times today.\n")

    def _onPremisesRec(self, pNode):
        if not pNode:
            return 0

        left_count = self._onPremisesRec(pNode.left) # returns counter value of left nodes
        right_count = self._onPremisesRec(pNode.right) # returns counter value of right nodes

        if pNode.attrCtr % 2 != 0:  # If the attrCtr is odd, player is on premises , checks for left and right nodes and sums up all the ID(nodes) with odd counter as onPremises Players
            return left_count + right_count + 1 
        else:
            return left_count + right_count

    def on_premises(self):
        count = self._onPremisesRec(self.root)

        with open('outputPS04.txt', 'a') as output_file:
            if count > 0:
                output_file.write(f"{count} players still on premises.\n")
            else:
                output_file.write("No players present on premises.\n")

    def _checkEmpRec(self, pNode, EId):
        if not pNode:
            return 0

        if EId == pNode.PId:
            if pNode.attrCtr % 2 != 0: # checks for counter value status is even or odd 
                return pNode.attrCtr, "in" # if even returns in to state inside hotel
            else:
                return pNode.attrCtr, "out" # if odd returns out to state outside hotel
        elif EId < pNode.PId:
            return self._checkEmpRec(pNode.left, EId)
        else:
            return self._checkEmpRec(pNode.right, EId)

    def check_employee(self, employee_id):
        result = self._checkEmpRec(self.root, employee_id)


        with open('outputPS04.txt', 'a') as output_file:
            if result:
                if result[1]=="in":
                    output_file.write(f"Player id {employee_id} swiped {result[0]} times today and is currently in hotel.\n")
                else :
                    output_file.write(f"Player id {employee_id} swiped {result[0]} times today and is currently outside hotel.\n")
            else:
                output_file.write(f"Player id {employee_id} did not swipe today.\n")


    def printRangePresent(self, StartId, EndId):
        with open('outputPS04.txt', 'a') as output_file:
            output_file.write(f"Range: {StartId} to {EndId}\n")
            output_file.write("Player swipe :\n")
            def inorder_traversal_range(node): #inorder traversal function to sort and print the ids along with their status within given range
                if node:
                    inorder_traversal_range(node.left)
                    if StartId <= node.PId <= EndId:
                        status = "in" if node.attrCtr % 2 != 0 else "out"
                        output_file.write(f"{node.PId}, {node.attrCtr}, {status}\n")
                    inorder_traversal_range(node.right)
            inorder_traversal_range(self.root)

def main():
    # Clearing the output file
    with open('outputPS04.txt', 'w') as output_file:
        pass  # Truncate the file

    BioB = BioBubble()

    try:
        # Read swipes from file
        BioB.read_swipes_from_file('inputPS04.txt')
        BioB._getSwipe()

        with open('promptsPS04.txt', 'r') as prompts_file:
            for line in prompts_file:
                line = line.strip()
                if line == 'onPremises:':
                    BioB.on_premises()
                elif line.startswith('checkPlay:'):
                    _, player_id = line.split(':')
                    player_id = int(player_id)
                    BioB.check_employee(player_id)
                elif line.startswith('freqVisit:'):
                    _, frequency = line.split(':')
                    frequency = int(frequency)
                    BioB.frequent_visitor(frequency)
                elif line.startswith('range:'):
                    range_str = line.split(' ')[1].strip()  # Use split() here
                    start, end = map(int, range_str.split(':'))
                    BioB.printRangePresent(start, end)
    except FileNotFoundError:
        print("Error: Input file not found.")
    except ValueError:
        print("Error: Invalid input format in the files.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
