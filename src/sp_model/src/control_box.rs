use sp_domain::*;
use sp_runner::*;

pub fn create_instance(name: &str) -> Resource {
    resource! {
        name: name,
        command!{
            topic: "goal",
            msg_type: "control_box_msgs/msg/Goal",

            run : bool,
            direction : bool,
            out1 : bool,
            out2 : bool,
        },
        measured!{
            topic: "measured",
            msg_type: "control_box_msgs/msg/Measured",

            sensor1 : bool,
            sensor2 : bool,
            button : bool,
        },

        transitions!{
            c_forward : p!([!run] || [direction]), vec![ a!(run), a!(!direction) ],
            c_backward : p!([!run] || [!direction]), vec![ a!(run), a!(direction) ],
            c_stop : p!(run), vec![ a!(!run) ],
        },
    }
}
