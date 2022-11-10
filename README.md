# substation_logger
A logger aka Historian for substation


Run Routine  
    Check for OPC configurations  
    Try to start OPC client  
    if failed, stop client with a message  
    If window is visible then show message to inform OPC client connection faliure

The software will run from Task Scheduler   
    No interaction from user  
    Software will fail if there is ill configured OPC parameteres

Software run usually by user   
    Check for OPC configurations  
    Try to start OPC client; if failed, stop client with a message

There should be a manaual button that starts the OPC client. 

If there is any change on the opc config then the OPC client should *restart*.





    