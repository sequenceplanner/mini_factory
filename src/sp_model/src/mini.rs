use failure::Error;
use sp_runner::*;


fn main() -> Result<(), Error> {
    let (model, initial_state) = mini();
    launch_model(model, initial_state)?;
    Ok(())
}

use sp_resources::*;
use sp_domain::*;

pub fn mini() -> (Model, SPState) {
    let mut m = GModel::new("mini");
    let ctrl = m.use_resource(control_box::create_instance("control_box"));

    let s1 = &ctrl["sensor1"];
    let s2 = &ctrl["sensor2"];
    let run = &ctrl["run"];
    let dir = &ctrl["direction"];

    let cyl_domain= &[
        "unknown".to_spvalue(),
        "inbetween".to_spvalue(),
        "at_left".to_spvalue(),
        "at_right".to_spvalue(),
    ];

    let cyl_pos = m.add_estimated_domain("cyl_pos", cyl_domain, true);

    m.add_effect("ev_left_sensor", &p!([p:cyl_pos != "unknown"] && [p:run] && [!p:dir] && [!p:s1]), &vec![a!(p:s1 = true)]);
    m.add_effect("ev_right_sensor", &p!([p:cyl_pos != "unknown"] && [p:run] && [p:dir] && [!p:s2]), &vec![a!(p:s2 = true)]);

    let timestamp = m.add_timestamp_variable("ctimestamp");
    let set_timestamp = Action::new(timestamp.clone(), Compute::TimeStamp);

    m.add_runner_transition("set_timestamp", &p!([p:s2 == true] && [p:timestamp == "reset"]), &vec![set_timestamp]);

    let ton = Predicate::TON(PredicateValue::path(timestamp.clone()),
                             PredicateValue::SPValue(SPValue::Int32(2000)));

    m.add_runner_transition("set_io_after_delay", &p!([pp: ton] && [!p:run]),
                            &vec![a!(p:run), a!(p:timestamp = "reset")]);


    m.add_op("to_left",
             // operation model guard.
             &p!(p:cyl_pos != "at_left"),
             // operation model effects.
             &[a!(p:cyl_pos = "at_left")],
             // low level goal
             &p!([p:s1] && [!p:run]),
             // low level actions (should not be needed)
             &[],
             // auto
             true, None);

    m.add_op("to_right",
             // operation model guard.
             &p!(p:cyl_pos != "at_right"),
             // operation model effects.
             &[a!(p:cyl_pos = "at_right")],
             // low level goal
             &p!([p:s2] && [!p:run]),
             // low level actions (should not be needed)
             &[],
             // auto
             true, None);



    let to_right = m.add_intention(
        "to_right",
        true,
        &p!(p:cyl_pos == "at_left"),
        &p!(p:cyl_pos == "at_right"),
        &[],
        None,
    );

    let to_left = m.add_intention(
        "to_left",
        true,
        &p!(p:cyl_pos == "at_right"),
        &p!(p:cyl_pos == "at_left"),
        &[],
        None,
    );


    // setup initial state of our estimated variables.
    // todo: do this interactively in some UI
    m.initial_state(&[
        (&cyl_pos, "unknown".to_spvalue()),
        (&to_right, "paused".to_spvalue()),
        (&to_left, "paused".to_spvalue()),
        (&timestamp, "reset".to_spvalue()),
    ]);

    println!("MAKING MODEL");
    m.make_model()
}

#[cfg(test)]
mod test {
    use super::*;
    use serial_test::serial;

    #[test]
    #[serial]
    fn cylinders_test() {
        let (m, s) = mini();

        make_new_runner(&m, s, true);

        println!("\n\n\n");
    }
}
