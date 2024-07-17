
def validate_optimal_ha_groups_parameters(active_bonus, number_of_members, sufficient_member_count, weight, lb1="active", lb2="standby"):
    print("\nValidation Results:");
    for lb1_active_member_count in range(number_of_members,-1,-1):
        for lb2_active_member_count in range(number_of_members,-1,-1):
            if lb1_active_member_count >= sufficient_member_count:
                if "active" in lb1:
                    lb1_score = active_bonus + weight;
                else:
                    lb1_score = weight;
            else:
                if "active" in lb1:
                    lb1_score = active_bonus + round(weight*(lb1_active_member_count/sufficient_member_count));
                else:
                    lb1_score = round(weight*(lb1_active_member_count/sufficient_member_count));            
            if lb2_active_member_count >= sufficient_member_count:
                if "active" in lb2:
                    lb2_score = active_bonus + weight;
                else:
                    lb2_score = weight;
            else:
                if "active" in lb2:
                    lb2_score = active_bonus + round(weight*(lb2_active_member_count/sufficient_member_count));
                else:
                    lb2_score = round(weight*(lb2_active_member_count/sufficient_member_count));
                    
            if lb1_score > lb2_score:
                lb1, lb2 = "active", "standby";
                print(f"LB1 Active Member Count: {lb1_active_member_count}, LB2 Active Member Count: {lb2_active_member_count}, LB1 Score: {lb1_score} (Active), LB2 Score: {lb2_score}");
            if lb1_score < lb2_score:
                lb1, lb2 = "standby", "active";
                print(f"LB1 Active Member Count: {lb1_active_member_count}, LB2 Active Member Count: {lb2_active_member_count}, LB1 Score: {lb1_score}, LB2 Score: {lb2_score} (Active)");
            if lb1_score == lb2_score:
                print("[-] Weight is inappropriate.");

def find_optimal_ha_groups_parameters():
    active_bonus = 1;
    number_of_members = int(input("\n[*] Provide number of port-channel members: "));
    minimum_member_count = 1;
    if number_of_members > 1:
        sufficient_member_count = number_of_members//2;
    else:
        sufficient_member_count = 1;
    for weight in range(0, 1000, 10):
        standby_score = weight;
        for active_member_count in range(number_of_members,-1,-1):
            if active_member_count >= sufficient_member_count:
                active_score = active_bonus + weight;
            else:
                active_score = active_bonus + round(weight*(active_member_count/sufficient_member_count));
            if ((active_score > standby_score) and (active_member_count >= sufficient_member_count)) or ((active_score < standby_score) and (active_member_count < sufficient_member_count)):
                continue;
            else:
                break;
        else:
            print(f"\nLB1:\nActive Bonus: {active_bonus}, Number of Members: {number_of_members}, Minimum Member Count: {minimum_member_count}, Sufficient Member Count: {sufficient_member_count}, Weight: {weight}");
            print(f"LB2:\nActive Bonus: {active_bonus}, Number of Members: {number_of_members}, Minimum Member Count: {minimum_member_count}, Sufficient Member Count: {sufficient_member_count}, Weight: {weight}");
            validate_optimal_ha_groups_parameters(active_bonus, number_of_members, sufficient_member_count, weight);
            break;

if "__main__" in __name__:
    find_optimal_ha_groups_parameters();
