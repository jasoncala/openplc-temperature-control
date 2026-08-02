PROGRAM main
  VAR
    Temperature : UINT AT %MW0 := 20;
    Fan : BOOL AT %QX0.0 := FALSE;
  END_VAR

(* Cooling fan control with 3-degree hysteresis. *)

IF Temperature >= 30 THEN
    Fan := TRUE;
ELSIF Temperature <= 27 THEN
    Fan := FALSE;
END_IF;

END_PROGRAM