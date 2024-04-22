""" Code blocks I may want to re-use / don't want to totally delete or have to hunt for in git history"""



def temp_distance_finding(boundary_coords): 
    
    lf_foulPole = boundary_coords['lf_foulPole']
    rf_foulPole = boundary_coords['rf_foulPole']
    cf_wall = boundary_coords['cf_wall']
    main_centroid = (950, 1430)
    
    a = cf_wall[0] - lf_foulPole[0]
    b = main_centroid[1] - cf_wall[1]
    c = helper.measure_distance_in_pixels(main_centroid, lf_foulPole)
    
    #print(f"\n    a = {a}, b = {b}, c = {c} \n") 
    
    min_diff = 10000
    best_y = None
    centre_x = 950

    dict = {}

    """
    for y in range(1100, 1700, 1):
        
        start_coord = (centre_x, y)    
        
        # Get distance to CF wall
        #cf_dist = helper.measure_distance_in_feet(start_coord, cf_wall)
        #rf_dist = helper.measure_distance_in_feet(start_coord, rf_foulPole)
        
        cf_dist = helper.measure_distance_in_pixels(start_coord, cf_wall)
        rf_dist = helper.measure_distance_in_pixels(start_coord, rf_foulPole)
        lf_dist = helper.measure_distance_in_pixels(start_coord, lf_foulPole)
        
        #curr_diff = abs(cf_dist - rf_dist)
        
        curr_diff = (cf_dist - rf_dist)**2 + (cf_dist - lf_dist)**2
        
        dict[y] = [round(curr_diff, 2), cf_dist]
        
        if curr_diff < min_diff:
            best_y = y
            min_diff = curr_diff
            dist = cf_dist

        #print(f"\ny = {y}, curr_diff = {round(curr_diff, 1)}\n" )    

    
    step_= 0 
    
    for key, value in dict.items(): 
        print(f"y={key} dist={value}  |  ", end = " ")
        step_ += 1
        if step_%5 == 0:
            print()

    print("\n    Best coord, dist: ", best_y, ", ", round(dist, 1), "\n")
    
    best_y = min(dict, key=dict.get)
    #best_dist = min(dict.values()[0])
             
    print(f"    Best y = {best_y}, shortest_distance = {round(best_dist, 1)}\n\n" )
    """    

#temp_distance_finding(boundary_coords)