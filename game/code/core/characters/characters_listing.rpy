init:
    default status_filters = set()
    default location_filters = set()
    default action_filters = set()
    default class_filters = set()
    python:
        def sorting_for_chars_list():
            return [c for c in hero.chars if c.is_available]

label chars_list:
    scene bg gallery
    # Check if we're the screen was loaded or not:
    if not renpy.get_screen("chars_list"):
        python:
            char_lists_filters = CharsSortingForGui(sorting_for_chars_list)
            char_lists_filters.filter()

            status_filters = set([c.status for c in hero.chars])
            # location_filters = set([c.location for c in hero.chars])
            home_filters = set([c.home for c in hero.chars])
            work_filters = set([c.workplace for c in hero.chars])
            action_filters = set([c.action for c in hero.chars])
            class_filters = set([bt for c in hero.chars for bt in c.traits.basetraits])
            selected_filters = set()
            the_chosen = set()

        show screen chars_list(source=char_lists_filters)
    with dissolve

    if not global_flags.has_flag("3_tutorial") and char_lists_filters.sorted:
        $ global_flags.set_flag("3_tutorial")
        show screen tutorial(3)

    python:
        while 1:

            result = ui.interact()

            if result[0] == 'control':
                if result[1] == 'return':
                    break
            elif result[0] == "dropdown":
                if result[1] == "workplace":
                    renpy.show_screen("set_workplace_dropdown", result[2], pos=renpy.get_mouse_pos())
                elif result[1] == "home":
                    renpy.show_screen("set_home_dropdown", result[2], pos=renpy.get_mouse_pos())
                elif result[1] == "action":
                    renpy.show_screen("set_action_dropdown", result[2], pos=renpy.get_mouse_pos())
            elif result[0] == 'choice':
                renpy.hide_screen("chars_list")
                char = result[1]
                jump('char_profile')

    hide screen chars_list
    jump mainscreen

screen chars_list(source=None):
    if not source.sorted:
        text "You don't have any workers.":
            size 40
            color ivory
            align .5, .2
            style "TisaOTM"

    key "mousedown_3" action Return(['control', 'return'])

    # Normalize pages.
    default page_size = 10
    default page = chars_list_last_page_viewed
    default tt = Tooltip("")

    $ max_page = len(source.sorted)/page_size-1
    if len(source.sorted)%page_size:
        $ max_page += 1
    if page > max_page:
        $ page = max_page

    python:
        listed_chars = []
        for start in xrange(0, len(source.sorted), page_size):
             listed_chars.append(source.sorted[start:start+page_size])

    # Chars:
    if listed_chars:
        $ charz_list = listed_chars[page]
        hbox:
            style_group "content"
            spacing 14
            pos (25, 60)
            xsize 970
            box_wrap True
            for c in charz_list:
                $ char_profile_img = c.show('portrait', resize=(98, 98), cache=True)
                $ img = "content/gfx/frame/ink_box.png"
                button:
                    ymargin 0
                    idle_background Frame(Transform(img, alpha=.4), 10 ,10)
                    hover_background Frame(Transform(img, alpha=.9), 10 ,10)
                    xysize (470, 115)
                    action Return(['choice', c])
                    hovered tt.Action('Show character profile')

                    # Image:
                    frame:
                        background Frame("content/gfx/frame/MC_bg3.png", 10, 10)
                        padding 0, 0
                        align 0, .5
                        xysize 100, 100
                        add char_profile_img align .5, .5 alpha .96

                    # Texts/Status:
                    frame:
                        xpos 120
                        xysize (335, 110)
                        background Frame(Transform("content/gfx/frame/P_frame2.png", alpha=.6), 10, 10)
                        label "[c.name]":
                            text_size 18
                            xpos 10
                            yalign .06
                            if c.__class__ == Char:
                                text_color pink
                            else:
                                text_color ivory

                        vbox:
                            align (.96, .035)
                            spacing 5
                            if c.status == "slave":
                                add ProportionalScale("content/gfx/interface/icons/slave.png", 40, 40)
                            else:
                                add ProportionalScale("content/gfx/interface/icons/free.png", 40, 40)

                        vbox:
                            align 1.0, .6 xoffset 5
                            hbox:
                                xsize 60
                                text "AP:" xalign .0 color ivory
                                text "[c.AP]" xalign .1 color ivory
                            hbox:
                                xsize 60
                                text "Tier:" xalign .0 color ivory
                                text "[c.tier]" xalign .1 color ivory
                            # text "AP: [c.AP]" size 17 color ivory
                            # text "Tier: [c.tier]" size 17 color ivory

                        vbox:
                            yalign .98
                            xpos 10
                            # Prof-Classes
                            python:
                                if len(c.traits.basetraits) == 1:
                                    classes = list(c.traits.basetraits)[0].id
                                elif len(c.traits.basetraits) == 2:
                                    classes = list(c.traits.basetraits)
                                    classes.sort()
                                    classes = ", ".join([str(t) for t in classes])
                                else:
                                    raise Exception("Character without prof basetraits detected! line: 211, chars_lists screen")
                            text "Classes: [classes]" color ivory size 18

                            null height 2
                            if c not in pytfall.ra:
                                if not c.flag("last_chars_list_geet_icon"):
                                    $ c.set_flag("last_chars_list_geet_icon", "work")
                                if c.status == "free" and c.flag("last_chars_list_geet_icon") != "work":
                                    $ c.set_flag("last_chars_list_geet_icon", "work")

                                if getattr(c.workplace, "is_school", False):
                                    button:
                                        style_group "ddlist"
                                        action NullAction()
                                        hovered tt.Action("%s is in training!" % c.nickname)
                                        text "{image=button_circle_green}Location: School"
                                else:
                                    if c.flag("last_chars_list_geet_icon") == "home":
                                        button:
                                            style_group "ddlist"
                                            if c.status == "slave":
                                                action Return(["dropdown", "home", c])
                                                hovered tt.Action("Choose a place for %s to live at (RMB to set Work)!" % c.nickname)
                                            else: # Can't set home for free cs, they decide it on their own.
                                                action NullAction()
                                                hovered tt.Action("%s is free and decides on where to live at!" % c.nickname)
                                            alternate [Function(c.set_flag, "last_chars_list_geet_icon", "work"),
                                                       Return(["dropdown", "workplace", c])]
                                            text "{image=button_circle_green}Home: [c.home]":
                                                if len(str(c.home)) > 18:
                                                    size 15
                                                else:
                                                    size 18
                                    elif c.flag("last_chars_list_geet_icon") == "work":
                                        $ tt_hint = "Choose a place for %s to work at" % c.nickname
                                        if c.status == "slave":
                                            $ tt_hint += " (RMB to set Home)!"
                                        else:
                                            $ tt_hint += "!"
                                        button:
                                            style_group "ddlist"
                                            action Return(["dropdown", "workplace", c])
                                            if c.status == "slave":
                                                alternate [Function(c.set_flag, "last_chars_list_geet_icon", "home"),
                                                           Return(["dropdown", "home", c])]
                                            hovered tt.Action(tt_hint)
                                            text "{image=button_circle_green}Work: [c.workplace]":
                                                if len(str(c.workplace)) > 18:
                                                    size 15
                                                else:
                                                    size 18
                                button:
                                    style_group "ddlist"
                                    action Return(["dropdown", "action", c])
                                    hovered tt.Action("Choose a task for %s to do!" % c.nickname)
                                    if getattr(c.workplace, "is_school", False):
                                        text "{image=button_circle_green}Action: [c.action.name] Course":
                                            if c.action.name is not None and len(str(c.action.name)) > 18:
                                                size 15
                                            else:
                                                size 18
                                    else:
                                        text "{image=button_circle_green}Action: [c.action]":
                                            if c.action is not None and len(str(c.action)) > 18:
                                                size 15
                                            else:
                                                size 18
                            else:
                                text "{size=15}Location: Unknown"
                                text "{size=15}Action: Hiding"

                    # Add to Group Button:
                    button:
                        style_group "basic"
                        xysize (25, 25)
                        align 1.0, 1.0 offset 9, -2
                        action ToggleSetMembership(the_chosen, c)
                        if c in the_chosen:
                            add(im.Scale('content/gfx/interface/icons/checkbox_checked.png', 25, 25)) align .5, .5
                        else:
                            add(im.Scale('content/gfx/interface/icons/checkbox_unchecked.png', 25, 25)) align .5, .5
                        hovered tt.Action('Select the character')

    # Filters:
    frame:
        background Frame(Transform("content/gfx/frame/p_frame2.png", alpha=.55), 10 ,10)
        style_prefix "content"
        xmargin 0
        left_padding 10
        ypadding 10
        pos (1005, 47)
        xysize (270, 468)
        vbox:
            spacing 3
            viewport:
                scrollbars "vertical"
                xsize 250
                draggable True
                mousewheel True
                has vbox xsize 253
                null height 5
                label "Filters:":
                    xalign .5
                    text_size 35
                    text_color goldenrod
                    text_outlines [(1, "#000000", 0, 0)]
                hbox:
                    box_wrap True
                    for f, c, t in [('Home', saddlebrown, 'Toggle home filters'),
                                    ('Work', brown, 'Toggle workplace filters'),
                                    ("Status", green, 'Toggle status filters'),
                                    ("Action", darkblue, 'Toggle action filters'),
                                    ('Class', purple, 'Toggle class filters')]:
                        button:
                            xalign .5
                            style_group "basic"
                            action ToggleSetMembership(selected_filters, f)
                            text f color c size 18 outlines [(1, "#3a3a3a", 0, 0)]
                            xpadding 6
                            hovered tt.Action(t)
                    button:
                        xalign .5
                        yalign 1.0
                        style_group "basic"
                        action source.clear, renpy.restart_interaction
                        text "Reset"
                        hovered tt.Action('Reset all filters')

                null height 20

                hbox:
                    box_wrap True
                    style_group "basic"
                    if "Status" in selected_filters:
                        for f in status_filters:
                            button:
                                xsize 125
                                action ModFilterSet(source, "status_filters", f)
                                text f.capitalize() color green
                                hovered tt.Action('Toggle the filter')
                    if "Home" in selected_filters:
                        for f in home_filters:
                            button:
                                xsize 125
                                action ModFilterSet(source, "home_filters", f)
                                text "[f]" color saddlebrown:
                                    if len(str(f)) > 12:
                                        size 12
                                hovered tt.Action('Toggle the filter')
                    if "Work" in selected_filters:
                        for f in work_filters:
                            button:
                                xsize 125
                                action ModFilterSet(source, "work_filters", f)
                                text "[f]" color brown:
                                    if len(str(f)) > 12:
                                        size 10
                                hovered tt.Action('Toggle the filter')
                    if "Action" in selected_filters:
                        for f in action_filters:
                            button:
                                xsize 125
                                action ModFilterSet(source, "action_filters", f)
                                $ t = str(f)
                                if t.lower().endswith(" job"):
                                    $ t = t[:-4]
                                text "[t]" color darkblue
                                hovered tt.Action('Toggle the filter')
                    if "Class" in selected_filters:
                        for f in class_filters:
                            button:
                                xsize 125
                                action ModFilterSet(source, "class_filters", f)
                                text "[f]" color purple
                                hovered tt.Action('Toggle the filter')
                # for block_name, filters in source.display_filters:
                    # label ("{=della_respira}{b}[block_name]:") xalign 0
                    # for item_1, item_2 in izip_longest(fillvalue=None, *[iter(filters)]*2):
                        # hbox:
                            # style_group "basic"
                            # for filter_item in [item_1, item_2]:
                                # if filter_item:
                                    # $ filter_name, filter_group, filter_key = filter_item
                                    # $ focus = source.get_focus(filter_group, filter_key)
                                    # button:
                                        # action [SelectedIf(focus), Function(source.add_filter, filter_group, filter_key)]
                                        # text "[filter_name]" size 16
            # Mass (de)selection Buttons ====================================>
            null height 3
            frame:
                background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=.9), 10, 10)
                xalign .5
                yalign .5
                # ypos 5
                xysize (250, 50)
                has hbox style_group "basic" align .5, .5 spacing 5
                hbox:
                    spacing 3
                    $ chars_on_page = set(charz_list) if hero.chars else set()
                    button: # select all on current listing, deselects them if all are selected
                        xysize (66, 40)
                        if the_chosen.issuperset(chars_on_page):
                            action SetVariable("the_chosen", the_chosen.difference(chars_on_page))
                        else:
                            action SetVariable("the_chosen", the_chosen.union(chars_on_page))
                        text "These"
                        hovered tt.Action('Select all currently visible characters')
                    button: # every of currently filtered, also in next tabs
                        xysize (66, 40)
                        action If(set(source.sorted).difference(the_chosen), [SetVariable("the_chosen", set(source.sorted))])
                        text "All"
                        hovered tt.Action('Select all characters')
                    button: # deselect all
                        xysize (66, 40)
                        action If(len(the_chosen), [SetVariable("the_chosen", set())])
                        text "None"
                        hovered tt.Action('Unselect everyone')
            # Mass action Buttons ====================================>
            frame:
                background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=.9), 10, 10)
                xalign .5
                yalign .5
                xysize (250, 145)
                has vbox style_group "basic" align .5, .5 spacing 3
                vbox:
                    spacing 3
                    button:
                        xysize (150, 40)
                        action If(len(the_chosen), [Show("char_control")])
                        text "Girl Control"
                        selected False
                        hovered tt.Action('Set desired behavior for group')
                    button:
                        xysize (150, 40)
                        action If(len(the_chosen), [Hide("chars_list"), With(dissolve), SetVariable("eqtarget", None), Jump('char_equip')])
                        text "Equipment"
                        selected False
                        hovered tt.Action('Manage group equipment')
                    button:
                        xysize (150, 40)
                        action If(len(the_chosen), [Hide("chars_list"), With(dissolve),
                                  Jump('school_training')])
                        text "Training"
                        selected False
                        hovered tt.Action('Manage group training')

    # Tooltips:
    frame:
        background Frame("content/gfx/frame/window_frame1.png", 10, 10)
        align(.09, 1.0)
        xysize (950, 65)
        text (u"{=content_text}{size=24}{color=[ivory]}%s" % tt.value) align(.5, .5)

    use top_stripe(True)

    # Two buttons that used to be in top-stripe:
    hbox:
        style_group "basic"
        pos 300, 5
        spacing 3
        textbutton "<--":
            sensitive page > 0
            action SetScreenVariable("page", page-1)
            hovered tt.Action('Previous page')
            keysym "mousedown_5"

        $ temp = page + 1
        textbutton "[temp]":
            xsize 40
            action NullAction()
        textbutton "-->":
            sensitive page < max_page
            action SetScreenVariable("page", page+1)
            hovered tt.Action('Next page')
            keysym "mousedown_4"

    $ store.chars_list_last_page_viewed = page # At Darks Request!
    # Normalize stored page, should we done 'on hide' but we can't trust those atm.
    if chars_list_last_page_viewed > max_page:
        $ chars_list_last_page_viewed = max_page
