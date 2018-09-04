init python:
    def items_transfer(it_members):
        renpy.show_screen("items_transfer", it_members)
        while 1:
            result = ui.interact()
            if isinstance(result, (list, tuple)):
                if result[0] == "control":
                    break
                elif result[0] == "transfer":
                    source, target, item, amount = result[1:]
                    for i in xrange(amount):
                        if not transfer_items(source, target, item):
                            break
        renpy.hide_screen("items_transfer")

    def it_on_show(it_members):
        for c in it_members:
            c.inventory.set_page_size(14)

    def it_on_hide(it_members):
        for c in it_members:
            c.inventory.set_page_size(15)

screen items_transfer(it_members):
    on "show":
        action Function(it_on_show, it_members)
    on "hide":
        action Function(it_on_hide, it_members)

    default lc = it_members[0]
    default source = it_members[0]
    default rc = it_members[1]
    default focused_item = None
    default transfer_amount = 1
    default slot_filter = it_members[0].inventory.slot_filter

    add "bg gallery"

    frame:
        style_group "dropdown_gm"
        xalign .5
        ypos 41
        xysize 250, 157
        text "Transfer Items between Characters!" align .5, .5 style "content_text" color ivory

    # Left/Right employment info:
    frame:
        background Frame("content/gfx/frame/p_frame5.png", 10, 10)
        style_group "dropdown_gm"
        xysize (1280, 45)
        if isinstance(lc, Char):
            text "[lc.traits.base_to_string] ---- [lc.action]" align (.09, .5) style "content_text" color ivory size 20
        if isinstance(rc, Char):
            text "[rc.traits.base_to_string] ---- [rc.action]" align (.92, .5) style "content_text" color ivory size 20

        use exit_button(size=(35, 35), align=(1.0, .5))

    key "mousedown_3" action Return(['control', 'return'])

    # Members + Items
    for scr_var, fc, xalign in [("lc", lc, .0), ("rc", rc, 1.0)]: # Focused characters...
        vbox:
            ypos 41
            spacing -4
            xalign xalign
            frame:
                background Frame("content/gfx/frame/p_frame5.png", 10, 10)
                padding 5, 5
                has viewport draggable True mousewheel True xysize 331, 300 child_size 330, 10000
                hbox:
                    spacing 1
                    box_wrap True
                    for c in it_members:
                        $ img = c.show("portrait", resize=(70, 70), cache=True)
                        vbox:
                            spacing 1
                            frame:
                                xpos 4
                                background Frame("content/gfx/frame/p_frame5.png", 10, 10)
                                xysize (162, 120)
                                imagebutton:
                                    align .5, .93
                                    style "basic_choice2_button"
                                    idle img
                                    hover img
                                    selected_idle Transform(img, alpha=1.05)
                                    action SetScreenVariable(scr_var, c), SelectedIf(c == fc), SensitiveIf(c != (rc if fc == lc else lc))
                                frame:
                                    xalign .5
                                    background Frame("content/gfx/frame/Mc_bg3.png", 5, 5)
                                    xysize(150, 22)
                                    ypadding 0
                                    if len(c.name) > 10:
                                        text "{color=[gold]}[c.name]" style "interactions_text" selected_color red size 14 outlines [(1, "#3a3a3a", 0, 0)] align .5, .5
                                    else:
                                        text "{color=[gold]}[c.name]" style "interactions_text" selected_color red size 20 outlines [(1, "#3a3a3a", 0, 0)] align .5, .5

            frame:
                background Frame("content/gfx/frame/p_frame5.png", 10, 10)
                style_group "dropdown_gm2"
                xysize 341, 375
                has vbox
                for item, amount in [(item, fc.inventory[item]) for item in fc.inventory.page_content]:
                    button:
                        xysize (330, 26)
                        action SensitiveIf(amount), SetScreenVariable("focused_item", item), SetScreenVariable("source", fc), SelectedIf(focused_item == item and source == fc)
                        text "[item.id]" align .0, .5 style "dropdown_gm2_button_text"
                        text "[amount]" align 1.0, .7 style "dropdown_gm2_button_value_text"

        # RC and LC Portraits:
    for fc, pos, xanchor in [(lc, (360, 43), 0), (rc, (920, 43), 1.0)]:
        frame:
            pos pos
            xanchor xanchor
            background Frame("content/gfx/frame/Mc_bg3.png", 10, 10)
            padding 1, 1
            add fc.show("portrait", resize=(150, 150), cache=True) align .5, .5

    frame:
        ypos 643
        xalign .5
        xysize (600, 80)
        background Frame("content/gfx/frame/p_frame5.png", 10, 10)
        hbox:
            yalign  .5
            spacing 210
            use paging(xysize=(190, 50), ref=lc.inventory, use_filter=False)
            use paging(xysize=(190, 50), ref=rc.inventory, use_filter=False)

    # Transfer Buttons:
    vbox:
        xalign .5
        ypos 653
        style_group "dropdown_gm"
        frame:
            xalign .5
            xysize 200, 30
            $ img = ProportionalScale('content/gfx/interface/buttons/left.png', 25, 25, align=(.5, .5))
            button:
                xysize (40, 30)
                style "default"
                align (0, .5)
                idle_background img
                hover_background im.MatrixColor(img, im.matrix.brightness(.15), align=(.5, .5))
                insensitive_background im.Sepia(img, align=(.5, .5))
                action SensitiveIf(rc.inventory[focused_item]), Return(["transfer", rc, lc, focused_item, transfer_amount]), SensitiveIf(focused_item)
                if lc and rc and focused_item:
                    tooltip "Transfer %s from %s to %s!" % (focused_item.id, rc.nickname, lc.nickname)

            $ img = ProportionalScale('content/gfx/interface/buttons/right.png', 25, 25, align=(.5, .5))
            button:
                xysize 40, 30
                style "default"
                align 1.0, .5
                idle_background img
                hover_background im.MatrixColor(img, im.matrix.brightness(.15), align=(.5, .5))
                insensitive_background im.Sepia(img, align=(.5, .5))
                action SensitiveIf(lc.inventory[focused_item]), Return(["transfer", lc, rc, focused_item, transfer_amount]), SensitiveIf(focused_item)
                if lc and rc and focused_item:
                    tooltip "Transfer %s from %s to %s!" % (focused_item.id, lc.nickname, rc.nickname)

        null height 1
        frame:
            xalign .5
            xysize 200, 30
            $ img = ProportionalScale('content/gfx/interface/buttons/blue_arrow_left.png', 25, 25, align=(.5, .5))
            button:
                xysize (40, 30)
                style "default"
                align 0, .5
                idle_background img
                hover_background im.MatrixColor(img, im.matrix.brightness(.15), align=(.5, .5))
                insensitive_background im.Sepia(img, align=(.5, .5))
                action SetScreenVariable("transfer_amount", 1 if transfer_amount - 5 < 1 else transfer_amount - 5)
                tooltip 'Decrease transfer amount by 5!'

            hbox:
                yalign .5
                spacing 5
                text 'Amount:' yalign .5 xpos 46 size 20 color ivory style "garamond"
                text '[transfer_amount]' yalign .5 xpos 60 size 18 color ivory style "proper_stats_value_text" yoffset -1

            $ img = ProportionalScale('content/gfx/interface/buttons/blue_arrow_right.png', 25, 25, align=(.5, .5))
            button:
                xysize 40, 30
                style "default"
                align 1.0, .5
                idle_background img
                hover_background im.MatrixColor(img, im.matrix.brightness(.15), align=(.5, .5))
                insensitive_background im.Sepia(img, align=(.5, .5))
                action SetScreenVariable("transfer_amount", transfer_amount + 5)
                tooltip 'Increase transfer amount by 5!'

    # Filters Buttons:
    frame:
        style_group "dropdown_gm"
        background Frame("content/gfx/frame/Mc_bg3.png", 10, 10)
        ypos 200
        padding 3, 3
        xalign .5
        has hbox spacing 1

        for filter in list(sorted(set(rc.inventory.filters + lc.inventory.filters))):
            $ img = ProportionalScale("content/gfx/interface/buttons/filters/%s.png" % filter, 40, 40)
            $ img_hover = ProportionalScale("content/gfx/interface/buttons/filters/%s hover.png" % filter, 40, 40)
            $ img_selected = ProportionalScale("content/gfx/interface/buttons/filters/%s selected.png" % filter, 40, 40)
            imagebutton:
                idle img
                hover im.MatrixColor(img_hover, im.matrix.brightness(.10))
                selected_idle img_selected
                selected_hover im.MatrixColor(img_selected, im.matrix.brightness(.10))
                action SetScreenVariable("slot_filter", filter), Function(rc.inventory.apply_filter, filter), Function(lc.inventory.apply_filter, filter), SelectedIf(filter == slot_filter)
                focus_mask True

    # Focused Item:
    if focused_item:
        frame:
            ypos 247
            xalign .5
            background Frame("content/gfx/frame/frame_dec_1.png", 10, 10)
            padding 30, 34
            use itemstats(item=focused_item, size=(540, 330))
