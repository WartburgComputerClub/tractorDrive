import bge

def portal(cont):
    # function courtesy of the YoFrankie folks
    own = cont.owner
    
    portal_ob = cont.sensors['portal_touch'].hitObject
    
    if not portal_ob:
        return
    #sce = bge.logic.getCurrentScene()
    #target_name = portal_ob['portal']

    # A bit dodgy, for the first logic tick show the loading text only
    # portal collision must be on pulse so its gets a second tick and runs the portal code below.
    for sce in bge.logic.getSceneList():
        if sce.name == 'hud':
            print('keys:',sce.objects)
            loading_ob = sce.objects['loading']#sce.objects['OBloading']
            if not loading_ob.visible:
                loading_ob.visible = True
                return
            
    
    set_blend_actu = cont.actuators['portal_blend']
    set_blend_actu.fileName = portal_ob['portal_blend']

    cont.activate(set_blend_actu)

def check_dead(cont):
        
    trac = cont.owner['handle'] 
    if trac.flipped():
        cont.activate(cont.actuators['restart_game'])
    elif trac.stuck():
        cont.activate(cont.actuators['restart_game'])
    elif trac.simFlag and trac.simFinished():
        cont.activate(cont.actuators['quit_game'])
    
def set_sim(cont):
    trac = cont.owner['handle']
    trac.setSim()
    
def update(a):
    car = a.owner
    trac = car['handle']


    wheel = car['wheel']
    if wheel.connected() and trac.active:
        wheel.update()
        trac.steer(wheel.getSteer())
        # Cruise control calculations
        cc = car['cc']
        cc.update()
        trac.setPower(cc.getPower())
        
    # should we make active
    if not trac.active and wheel.connected():
        prev = wheel.getSteer()
        wheel.update()
        if abs(prev - wheel.getSteer()) > .01:
            if trac.stuckCount > 2:
                trac.active = True
                car['cc'].reset()      # reset cruise control (time drift)
                trac.stuckCount = 0
                
            else:
                trac.stuckCount += 1