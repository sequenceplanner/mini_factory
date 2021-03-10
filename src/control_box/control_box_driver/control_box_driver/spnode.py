import json

from rclpy.node import Node
from sp_messages.msg import RegisterResource
from sp_messages.msg import Resources

class SPNode(Node):
    def __init__(self, node_name):
        super().__init__(node_name)

        # Resource
        self.resource = RegisterResource()
        # hack för att köra utan namespace
        self.resource.path = "conveyor" # self.get_namespace()
        self.resource.model = ""
        self.resource.last_goal_from_sp = ""

        self.sp_node_cmd_subscriber = self.create_subscription(
            Resources,
            "/sp/resources",
            self.sp_resources_callback
            )#,10)

        self.sp_resource_publisher = self.create_publisher(
            RegisterResource,
            "/sp/resource"
            )#, 10)

    def sp_resources_callback(self, data):
        if not self.resource.path in data.resources:
            self.get_logger().info('The resource ' + str(self.resource.path) + ' is not registered in :' + str(data.resources))
            self.sp_resource_publisher.publish(self.resource)

    def goal_to_json(self, msg_type, goal):
        # hack för att get_fields inte finns i bouncy
         # move to general function in sp
        # goal_to_json = {}
        # for k in msg_type.get_fields_and_field_types().keys():
        #     goal_to_json.update({k: getattr(goal, "_"+k)})

        goal_to_json = {
            "run": False,
            "direction": False,
            "out1": False,
            "out2": False,
        }

        self.resource.last_goal_from_sp = json.dumps(goal_to_json)

    def has_last_goal(self):
        return bool(self.resource.last_goal_from_sp)
