PROGRAM main
VAR
    Temperature AT %MW0 : UINT := 20;
    Fan AT %QX0.0 : BOOL := FALSE;
END_VAR

(* Cooling fan control with 3-degree hysteresis. *)

IF Temperature >= 30 THEN
    Fan := TRUE;
ELSIF Temperature <= 27 THEN
    Fan := FALSE;
END_IF;

END_PROGRAM


CONFIGURATION Config0

RESOURCE Res0 ON PLC

    TASK MainTask(
        INTERVAL := T#20ms,
        PRIORITY := 0
    );

    PROGRAM MainInstance
        WITH MainTask
        : main;

END_RESOURCE

END_CONFIGURATION