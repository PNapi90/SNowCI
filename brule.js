(function executeRule(current, previous /*null when async*/)
{

    // Add your code here
    var users = new GlideRecord('sys_user');
    users.query();
    var count = users.getRowCount();


    gs.info("Users",count);
    var random = Math.floor((Math.random() * count));
    var userNum = 0;
    gs.info(random);
    while(users.next())
    {
        if(userNum == random)
        {
            gs.info("Doer " + current.doer + " SU: " +  current.doit_supervisor);
            gs.info(users.name + " " +users.sys_id + " " + random);
            current.doit_supervisor = users.sys_id;
            //gs.info(current.update());
            gs.info("SET IN " + current.number + " -> " + current.doit_supervisor.name);
            break;
        }
        //gs.info(users.name," ", userNum);
        userNum += 1;
    }   
})(current, previous);