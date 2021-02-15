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
    let conv = m.use_named_resource("conv", conv::create_instance("conv"));

    let s1 = &conv["s1"];
    let s2 = &conv["s2"];
    let dir = &conv["dir"];
    let act_dir = &conv["act_dir"];

    let cyl_domain= &[
        "unknown".to_spvalue(), 
        "inbetween".to_spvalue(), 
        "at_left".to_spvalue(),
        "at_right".to_spvalue(),
    ];

    let cyl_pos = m.add_estimated_domain("cyl_pos", cyl_domain, true);

    m.add_effect("ev_left_sensor", p!([cyl_pos != "unknown"] && [act_dir == "left"]), a!(s1 = true));
    m.add_effect("ev_right_sensor", p!([cyl_pos != "unknown"] && [act_dir == "right"]), a!(s2 = true));

    m.add_auto("at_left", p!([s1] && [cyl_pos != "at_left"]), vec!(a!(cyl_pos = "at_left")));
    m.add_auto("at_right", p!([s2] && [cyl_pos != "at_right"]), vec!(a!(cyl_pos = "at_right")));
    m.add_auto("at_inbetween", p!([!s1] && [!s2] && [[cyl_pos == "at_left"] ||[cyl_pos == "at_right"]]), vec!(a!(cyl_pos = "inbetween")));


    


    // setup initial state of our estimated variables.
    // todo: do this interactively in some UI
    m.initial_state(&[
        
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
