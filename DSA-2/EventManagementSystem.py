from datetime import datetime
class Event:
    def __init__(self, event_id, start_time, end_time, event_name):
        self.event_id = event_id
        self.start_time = start_time
        self.end_time = end_time
        self.event_name = event_name

class AVLNode:
    def __init__(self, event):
        self.event = event
        self.height = 1
        self.left = None
        self.right = None

class AVLTree:
    def __init__(self):
        self.root = None

    # def print_tree(self):
    #     self._print_inorder(self.root)
        
        
    
    # def _print_inorder(self, node):
    #     if node is None:
    #         return
    #     self._print_inorder(node.left)
    #     print(f"Event ID: {node.event.event_id}, Start Time: {node.event.start_time}, End Time: {node.event.end_time}, Event Name: {node.event.event_name}")
    #     self._print_inorder(node.right)

    def insert(self, event):
       
        self.root = self._insert(self.root, event)
        if self.root is None:
            print(f"Event does not exist.")

    def _insert(self, node, event):
        
        if not node:
            return AVLNode(event)
        
        if event.event_id < node.event.event_id:
            node.left = self._insert(node.left, event)
        else:
            node.right = self._insert(node.right, event)
        
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
        
        balance = self._get_balance(node)
        
        # Left Left Case
        if balance > 1 and event.event_id < node.left.event.event_id:
            return self._rotate_right(node)
        
        # Right Right Case
        if balance < -1 and event.event_id > node.right.event.event_id:
            return self._rotate_left(node)
        
        # Left Right Case
        if balance > 1 and event.event_id > node.left.event.event_id:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        
        # Right Left Case
        if balance < -1 and event.event_id < node.right.event.event_id:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)
        
        return node
    
    def delete(self, event_id):
        self.root = self._delete(self.root, event_id)
        if self.root is None:
            print(f"Event with ID {event_id} does not exist.")
            return
    
    def _delete(self, node, event_id):
        if not node:
            return node

        if event_id < node.event.event_id:
            node.left = self._delete(node.left, event_id)
        elif event_id > node.event.event_id:
            node.right = self._delete(node.right, event_id)
        else:
            if not node.left:
                temp = node.right
                node = None
                return temp
            elif not node.right:
                temp = node.left
                node = None
                return temp

            temp = self._get_min_value_node(node.right)
            node.event = temp.event
            node.right = self._delete(node.right, temp.event.event_id)

        if not node:
            return node

        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))

        balance = self._get_balance(node)

        # Left Left Case
        if balance > 1 and self._get_balance(node.left) >= 0:
            return self._rotate_right(node)

        # Left Right Case
        if balance > 1 and self._get_balance(node.left) < 0:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)

        # Right Right Case
        if balance < -1 and self._get_balance(node.right) <= 0:
            return self._rotate_left(node)

        # Right Left Case
        if balance < -1 and self._get_balance(node.right) > 0:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    
    def search(self, event_id):
        return self._search(self.root, event_id)

    

    def _search(self, node, event_id):
        if not node:
            return None
        
        event_id = event_id

        if node.event.event_id == event_id:
            return node.event
        
        if event_id < node.event.event_id:
            return self._search(node.left, event_id)
        else:
            return self._search(node.right, event_id)

    def search_events_within_range(self, start_time, end_time):
        result = []
        self._search_within_range(self.root, start_time, end_time, result)
        return result

    def _search_within_range(self, node, start_time, end_time, result):
        if node is None:
            return
        
        sorted_list= self.inorder_sorted_events(node)
        #print(sorted_list)

        for obj in sorted_list:
            #print(start_time,obj[1],end_time,obj[2],obj[0],obj[3])
            if(start_time < obj[1] < end_time or start_time < obj[2] < end_time):
                #print(node.event.event_id)
                result.append(obj)


    def _get_height(self, node):
        if not node:
            return 0
        return node.height

    def _get_balance(self, node):
        if not node:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)

    def _rotate_right(self, z):
        y = z.left
        T3 = y.right
        
        y.right = z
        z.left = T3
        
        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
        
        return y

    def _rotate_left(self, z):
        y = z.right
        T2 = y.left
        
        y.left = z
        z.right = T2
        
        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
        
        return y

    def _get_min_value_node(self, node):
        current = node
        while current.left:
            current = current.left
        return current
    
    def preOrder(self, node):
        if not node:
            return
        print("{0} ".format(node.event.event_id), end="")
        self.preOrder(node.left)
        self.preOrder(node.right)

    def inorder_sorted_events(self,node):
        sorted_events = []
        self._inorder_sorted_events(node, sorted_events)
        return sorted_events
    
    def _inorder_sorted_events(self,node,sorted_events):
        if node is None:
            return

        self._inorder_sorted_events(node.left, sorted_events)
        sorted_events.append((node.event.event_id,node.event.start_time,node.event.end_time,node.event.event_name))
        self._inorder_sorted_events(node.right, sorted_events)

with open("outputPS04.txt", "w") as output_file:

    def addEvent(event_ID="", start_time="", end_time="", event_name=""):
        event = Event(event_ID, start_time, end_time, event_name)
        output_file.write(f"ADDED: {event_ID} - {event_name}\n")
        return event

    def removeEvent(event_ID=""):
        event = avl_tree.search(event_ID)
        if event:
            avl_tree.delete(event_ID)
            output_file.write(f"REMOVED: {event_ID} - {event.event_name}\n")
        else:
            output_file.write("Event to be removed not found\n")

    def searchEvent(event_ID=""):
        event_node = avl_tree.search(event_ID)
        if event_node:
            event_start=event_node.start_time.strftime("%d/%m/%Y %H:%M:%S")
            event_end=event_node.end_time.strftime("%d/%m/%Y %H:%M:%S")
            output_file.write(f"SEARCHED: {event_ID}\n")
            output_file.write(f"-----------------------------------------------------------------------------------------\n")
            output_file.write(f"{event_node.event_id} - {event_start} - {event_end} - {event_node.event_name}\n")
            output_file.write(f"-----------------------------------------------------------------------------------------\n")
        else:
            output_file.write("Event not found!\n")
    
    def searchEventByRange(start_time="", end_time=""):
        events_within_range = avl_tree.search_events_within_range(start_time, end_time)
        # output_file.write("Events within the specified range:\n")
        if events_within_range:
                start_format = datetime.strftime(start_time, "%d/%m/%Y %H:%M:%S")
                end_format = datetime.strftime(end_time, "%d/%m/%Y %H:%M:%S")
                # output_file.write(f"SEARCHED: Events from {start_time} to {end_time}\n")
                output_file.write(f"SEARCHED: Events from {start_format} to {end_format}\n")
                output_file.write(f"-----------------------------------------------------------------------------------------\n")
                for event in events_within_range:
                    #event_start=event.start_time.strftime("%d/%m/%Y %H:%M:%S")
                    #event_end=event.end_time.strftime("%d/%m/%Y %H:%M:%S")
                    output_file.write(f"{event[0]} - {event[1]} - {event[2]} - {event[3]}\n")
                output_file.write(f"-----------------------------------------------------------------------------------------\n")

    def initiateEventManagementSystem(read_input_file):

        with open(read_input_file, 'r') as file:
            for line in file:
                parts = line.strip().split(': ', 1)
                command = parts[0].strip()
                arguments = parts[1].strip().split(' - ')
                
                if command == 'Add Event':
                    try:
                        event_id, start_time1, end_time1, event_name = map(str.strip, arguments)
                        dtime1 = datetime.strptime(start_time1, "%d/%m/%Y %H:%M:%S")
                        dtime2 = datetime.strptime(end_time1, "%d/%m/%Y %H:%M:%S")
                        # start_time = dtime1.strftime("%d/%m/%Y %H:%M:%S")
                        # end_time= dtime2.strftime("%d/%m/%Y %H:%M:%S")
                        event = addEvent(event_ID= event_id,start_time=dtime1, end_time=dtime2, event_name=event_name)
                        avl_tree.insert(event)

                    except ValueError:
                        print("Invalid date format")

                elif command == 'Remove Event':
                    event_id = arguments[0]
                    removeEvent(event_ID=event_id)

                elif command == 'Search Event by ID':
                    event_id = arguments[0]
                    searchEvent(event_ID=event_id)

                elif command == 'Search Event by Range':
                    start_time1, end_time1 = map(str.strip, arguments)
                    dtime1 = datetime.strptime(start_time1, "%d/%m/%Y %H:%M:%S")
                    dtime2 = datetime.strptime(end_time1, "%d/%m/%Y %H:%M:%S")
                    # start_time = dtime1.strftime("%d/%m/%Y %H:%M:%S")
                    # end_time= dtime2.strftime("%d/%m/%Y %H:%M:%S")
                    searchEventByRange(start_time=dtime1, end_time=dtime2)

        return avl_tree

    avl_tree = AVLTree()
    avl_tree = initiateEventManagementSystem("inputPS04.txt")
    #avl_tree.print_tree()

    def inorder_sorted_events(node):
        sorted_events = []
        _inorder_sorted_events(node, sorted_events)
        return sorted_events
    def _inorder_sorted_events(node, sorted_events):
        if node is None:
            return

        _inorder_sorted_events(node.left, sorted_events)
        sorted_events.append((node.event.event_id,node.event.start_time,node.event.end_time))
        _inorder_sorted_events(node.right, sorted_events)

    # sorted_events_list = inorder_sorted_events(avl_tree.root)
    # for obj in sorted_events_list:
    #     


    