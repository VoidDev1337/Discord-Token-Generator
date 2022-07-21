'''
        global solved
        payload = { "proxy": proxy, "siteUrl" : site_url, "siteKey":site_key, "threadId" : thread_id, "canBeSolveInOneClick"  : can_solve_in_one_click }
        
        try:
            response = requests.post(solver_address, json=payload)
        except:
            Logger.Error(f"Can't get access to the solver url ({solver_address})")
            return False
        
        captcha_key = response.text
        
        if "P0_" in captcha_key:
            solved += 1
            ctypes.windll.kernel32.SetConsoleTitleW(f"Space Token Generator - Started... | Auto Joining : discord.gg/{config['invite_code']} | Captchas Solved : {solved}")
            #Logger.Success("Solved Captcha")
            return captcha_key
        else:
            return False
'''