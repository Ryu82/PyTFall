screen pyp_general():
    zorder 1001

    fixed:
        pos 302, 49
        xysize 971, 664
        style_prefix "pyp"

        add "content/gfx/interface/logos/logo9.png" xalign .5 ypos 30

        vbox:
            align .5, .5
            label "Open World H/Sim Game"
            text ("PyTFall is an open source, turn-based Sim game with a Hentai twist"+
                  " developed to serve as a next-generation of WM and SimBro focusing on "+
                  "gathering a team of workers, managing businesses, leveling up "+
                  "the MC and other characters and Date-Sim Elements, "+
                  "RPG Style Combat and Exploration, Interactions and etc.")
            null height 10
            text ("Events of PyTFall take place in the same universe as those of WM"+
                  " (Whore Master). The world itself poses barely any rules or"+
                  " guidelines to it. The WM's original City (CrossGate) still "+
                  "exists in the time frame of PyTFall and is described as "+
                  "'the slave capital of the World'.")
            null height 10
            text ("In the future, we're hoping to expand it with many more cities, businesses, gang-fighting, "+
                  "Politics that have a direct effect on game world rules (such as slavery being forbidden, slaves not"+
                  " being able to part-take in combat, prostitution banned and etc.), Economy, Religions, World Events, and much more.")

    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.webp"

screen pyp_time_flow():
    zorder 1001

    fixed:
        pos 302, 49
        xysize 971, 664
        style_prefix "pyp"
        fixed:
            xysize 600, 664
            # Title and text bits:
            frame:
                style_suffix "title_frame"
                xalign .5 ypos 10
                text "Time Flow" size 30

            vbox:
                ypos 80
                text ("One turn of the game corresponds to one day, in which the Player"+
                      " can take actions, perform tasks, jobs and date-sim to his/her heart's content.")
                null height 10
                text ("There is presently no concept of daytimes (Morning/Day/Evening/Night)"+
                      " in PyTFall, although we develop with a presence of those in mind. A large amount of"+
                      " extra content (mostly backgrounds) that would be required is scary and not reasonable to mess"+
                      " around with at this development stage.")

        fixed:
            xpos 601
            xysize 370, 664
            style_prefix "pyp"
            add pscale("content/gfx/interface/icons/clock.png", 250, 250):
                xalign .5 ypos 50

    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.webp"

screen pyp_action_points():
    zorder 1001

    fixed:
        pos 302, 49
        xysize 971, 664
        style_prefix "pyp"
        fixed:
            xysize 600, 664
            # Title and text bits:
            frame:
                style_suffix "title_frame"
                xalign .5 ypos 10
                text "Action Points" size 30

            text ("Actions Points decide how many actions "+
                  "the Player and other Characters can take per one game turn (Day). "+
                  " The amount of AP depends on stats (constitution) and Traits."+
                  " When performing Jobs during the Next Day, 'AP' is converted to Job Points (1 AP = 100 JP)"+
                  " that can be affected by Upgrades and Manager effects. For Interactions,"+
                  " AP is converted into Interaction Points (1 AP = 3 IP)"):
                      ypos 80


        fixed:
            xpos 601
            xysize 370, 664
            style_prefix "pyp"
            frame:
                xalign .5 ypos 105
                add pscale("content/gfx/interface/pyp/ap.webp", 250, 100)

    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.webp"

screen pyp_next_day():
    zorder 1001

    fixed:
        pos 302, 49
        xysize 971, 664
        style_prefix "pyp"
        fixed:
            xysize 600, 664
            # Title and text bits:
            frame:
                style_suffix "title_frame"
                xalign .5 ypos 10
                text "Next Day" size 30

            vbox:
                ypos 80
                text ("Next Day starts execution of businesses, training and some events"+
                      " pushing the game to the next day.")
                null height 10
                text ("For any Character (including the Player itself), Next Day will execute whatever 'Action'"+
                      " they are set to perform and spend the remaining amount of Action Points performing it. "+
                      " At the end of such a cycle, you will be able to review detailed reports of everything that has happened "+
                      " as those actions and events were performed.")

        fixed:
            xpos 601
            xysize 370, 664
            style_prefix "pyp"
            vbox:
                xalign .5 ypos 80
                spacing 20
                frame:
                    xalign .5
                    add pscale("content/gfx/interface/pyp/next_day_button.webp", 350, 1000)
                frame:
                    xalign .5
                    add pscale("content/gfx/interface/pyp/next_day_screen.webp", 350, 1000)

    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.webp"

screen pyp_gazette():
    zorder 1001

    fixed:
        pos 302, 49
        xysize 971, 664
        style_prefix "pyp"
        fixed:
            xysize 600, 664
            # Title and text bits:
            frame:
                style_suffix "title_frame"
                xalign .5 ypos 10
                text "PyTFall GAZETTE" size 30

            vbox:
                ypos 80
                text ("Gazzete reports on major events in the city!")
                null height 10
                text ("It will be significantly expanded once we have World Events, "+
                      "Politics, and Economy. For now, you will know about the events at the Arena, "+
                      " shop and slave market restocks and new workers submitting their applications to"+
                      " the Employment agency!")

        fixed:
            xpos 601
            xysize 370, 664
            style_prefix "pyp"
            frame:
                xalign .5 ypos 90
                add "content/gfx/interface/pyp/gazette.webp" align .5, .05

    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.webp"
