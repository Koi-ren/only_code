          
            if close >= 1:
                if (left == True) and (mid == True) and (right  == False)
                    stop_car(10)
                    drive(30, 10)
                    time.sleep(3)
                    drive(-30, 10)
                    time.sleep(6)
                    drive(30, 10)
                    time.sleep(3)
    
                if (left == False) and (mid == True) and (right == True)
                    stop_car(10)
                    drive(-30, 10)
                    time.sleep(3)
                    drive(30, 10)
                    time.sleep(6)
                    drive(-30, 10)
                    time.sleep(3)