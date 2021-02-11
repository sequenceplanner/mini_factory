use sp_domain::*;
use sp_runner::*;

pub fn create_instance(name: &str) -> Resource {
    resource! {
        name: name,
        command!{
            topic: "goal",
            msg_type: "json",

            dir : vec!["left", "right", "stop"],
        },
        measured!{
            topic: "state",
            msg_type: "json",

            act_dir : vec!["left", "right", "stop"],
            s1 : bool,
            s2 : bool,
        },
        estimated!{

        },
        predicates!{
            stopped: p!([dir == "stop"] && [act_dir == "stop"]),
            stopping: p!([dir == "stop"] && [act_dir != "stop"]),
        },

        transitions!{
            c_left : p!([stopped]), vec![ a!(dir = "left") ],
            e_finish_left : p!([dir == "left"] && [act_dir != "left"]), vec![a!(act_dir = "left")],
            c_right : p!([stopped]), vec![ a!(dir ="right") ],
            e_finish_right : p!([dir == "right"] && [act_dir != "right"]), vec![a!(act_dir = "right")],
            c_stop : p!([!stopped]), vec![ a!(dir ="stop") ],
            e_finish_stop : p!([dir == "stop"] && [act_dir != "stop"]), vec![a!(act_dir = "stop")],

        },

    }
}