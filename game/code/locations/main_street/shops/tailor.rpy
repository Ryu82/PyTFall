label tailor_store:
    
    # Music related:
    if not "shops" in ilists.world_music:
        $ ilists.world_music["shops"] = [track for track in os.listdir(content_path("sfx/music/world")) if track.startswith("shops")]
    if not global_flags.has_flag("keep_playing_music"):
        play world choice(ilists.world_music["shops"]) fadein 1.5

    hide screen main_street
    
    scene bg tailor_store
    with dissolve
    
    $ t = npcs["Kayo_Sudou"].say
        
    if global_flags.flag('visited_tailor_store'):
        show expression npcs["Kayo_Sudou"].get_vnsprite() as npc
        with dissolve
        t "Welcome back, take a look at our latest arrivals!"

    else:
        $global_flags.set_flag('visited_tailor_store')
            
        "You entered the shop. The shelves are filled with colourful silks and some exquisite dresses are displayed on the mannequins. Noticing your arrival, a tailor lady comes in from the back room and approaches you."
 
        show expression npcs["Kayo_Sudou"].get_vnsprite() as npc
        with dissolve
        
        t "Oh, a new customer! Welcome to my store."
        t "I'm honored to present you our wares. All pieces you see were acquired from the most renowned merchants. "
        t "But If you have any special requests, just tell me. I'm sure I will be able to help you."
        
label tailor_menu: # after she said her lines but before we show menu controls, to return here when needed
    show screen tailor_shop
    with dissolve
    while 1:
        $ result = ui.interact()

    
label tailor_store_shopping:
    python:
        focus = False
        item_price = 0
        filter = "all"
        amount = 1
        shop = pytfall.tailor_store
        shop.inventory.apply_filter(filter)
        char = hero
        char.inventory.set_page_size(18)
        char.inventory.apply_filter(filter)

    show screen shopping(left_ref=hero, right_ref=shop)
    with dissolve
    call shop_control from _call_shop_control_4
    
    $ global_flags.del_flag("keep_playing_music") 

    hide screen shopping
    with dissolve
    jump tailor_menu
            
screen shopkeeper_items_upgrades(upgrades_list):
    modal True
    frame:
        align (0.5, 0.5)
        background Frame("content/gfx/frame/frame_dec_1.png", 75, 75)
        xpadding 75
        ypadding 75
        has vbox
        text "Upgrades" style "proper_stats_value_text" outlines [(1, "#181818", 0, 0)] color "#DAA520" size 30 yalign .5 xalign .5
        null height 15
        for i in upgrades_list:
            frame:
                style_prefix "wood"
                background Frame("content/gfx/frame/cry_box.png", 5, 5)
                xpadding 10
                ypadding 10
                hbox:
                    spacing 0
                    xsize 600
                    xalign 0.5
                    vbox:
                        add ProportionalScale(items[i[0]].icon, 80, 80) xalign 0.5
                        text "%s" %i[0] style "proper_stats_value_text" outlines [(1, "#181818", 0, 0)] color "#DAA520" size 15 xalign 0.5
                    text "+ %s GP =" %i[1] style "proper_stats_value_text" outlines [(1, "#181818", 0, 0)] color "#DAA520" size 25 yalign .5 xalign 0.0
                    add ProportionalScale(items[i[2]].icon, 80, 80) xalign 0.5
                    null width 10
                    button:
                        xysize (100, 50)
                        xalign 1.0
                        yalign 0.5
                        text "Order" size 16 color goldenrod
                        action Return(upgrades_list.index(i))
                        padding (10, 10)
                    null height 1
        null height 5
        button:
            xysize (180, 50)
            style_prefix "wood"
            text "Cancel" size 16 color goldenrod
            xalign 0.5
            action Return(-1)

label tailor_special_order:
    if npcs["Kayo_Sudou"].has_flag("tailor_special_order"):
        if day - npcs["Kayo_Sudou"].flag("tailor_special_order")[0] < 3:
            t "I'm very sorry, your order is not ready yet. Please come later."
        else:
            $ i = int(npcs["Kayo_Sudou"].flag("tailor_special_order")[1])
            $ j = upgrade_list[i][2]
            t "Yes, your order is ready. *she gives you [j]*"
            $ hero.add_item(upgrade_list[i][2])
            $ del i
            $ del j
            t "Ask anytime if you need anything else!"
            $ npcs["Kayo_Sudou"].del_flag("tailor_special_order")
    else:
        t "For a small price I can upgrade your clothes to better versions. What would you like to order?"
        $ upgrade_list = [["Casual Clothes", 40, "Armored Casual Clothes"], ["Artisan Outfit", 200, "Elite Artisan Outfit"], ["Leather Jacket", 600, "Altered Leather Jacket"], ["Mercenary Clothes", 900, "Proper Mercenary Clothes"]]
        # TODO: load the list of upgrades from json instead of this hardcoded list
        $ result = renpy.call_screen("shopkeeper_items_upgrades", upgrade_list)
        # t "[result]"
        if result == -1:
            t "If you want anything, please don't hesitate to tell me."
        else:
            if has_items(upgrade_list[result][0], [hero], equipped=False) <= 0:
                t "I'm sorry, you don't have the required base item. Please make sure to unequip it if it's equipped."
            elif hero.take_money(upgrade_list[result][1], reason="Tailor Upgrade"):
                $ hero.remove_item(upgrade_list[result][0])
                t "Of course, dear customer, it will be ready in three days. You can retrieve your order in our shop after the time passes."
                $ npcs["Kayo_Sudou"].set_flag("tailor_special_order", value=[day, result])
            else:
                t "I'm sorry, but you don't have that much gold."
    jump tailor_menu
    
screen tailor_shop:
    frame:
        xalign 0.95
        ypos 20
        background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=0.98), 10, 10)
        xpadding 10
        ypadding 10
        vbox:
            style_group "wood"
            align (0.5, 0.5)
            spacing 10
            button:
                xysize (150, 40)
                yalign 0.5
                action [Hide("tailor_shop"), Jump("tailor_store_shopping")]
                text "Shop" size 15
            button:
                xysize (150, 40)
                yalign 0.5
                action [Hide("tailor_shop"), Jump("tailor_special_order")]
                text "Special Order" size 15
            button:
                xysize (150, 40)
                yalign 0.5
                action [Hide("tailor_shop"), Jump("main_street")]
                text "Leave" size 15