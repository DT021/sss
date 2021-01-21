#################################################
# V45 - Author: Asaf Ravid <asaf.rvd@gmail.com> #
#################################################


import sss_filenames
import csv
import os


def get_row_index(ticker_index, ticker, rows):
    index = 0
    for row in rows:
        if ticker == row[ticker_index]:
            return index
        index += 1
    return -1


def run(newer_path, older_path, db_exists_in_both_folders, diff_only_recommendation, ticker_index, name_index, movement_threshold, newer_rec, older_rec, rec_length):
    newer_filenames_list = sss_filenames.create_filenames_list(newer_path)
    older_filenames_list = sss_filenames.create_filenames_list(older_path)
    diff_path = 'Results/diff'+'_new'+newer_path.replace('Results/','_')+'_old'+older_path.replace('Results/','_')
    compact_diff_path = diff_path.replace('FavorTechBy3','FTB3').replace('MCap_','').replace('BuildDb_','').replace('nResults','')
    diff_filenames_list  = sss_filenames.create_filenames_list(compact_diff_path)
    #                                                                              evr_min,      evr_max,      pm_min,       pm_max
    newer_filenames_list.insert(0,newer_path+'/recommendation_ssss_evr{}-{}_pm{}-{}.csv'.format( newer_rec[0], newer_rec[1], newer_rec[2], newer_rec[3]))
    newer_filenames_list.insert(0,newer_path+'/recommendation_sssss_evr{}-{}_pm{}-{}.csv'.format(newer_rec[0], newer_rec[1], newer_rec[2], newer_rec[3]))
    older_filenames_list.insert(0,older_path+'/recommendation_ssss_evr{}-{}_pm{}-{}.csv'.format( older_rec[0], older_rec[1], older_rec[2], older_rec[3]))
    older_filenames_list.insert(0,older_path+'/recommendation_sssss_evr{}-{}_pm{}-{}.csv'.format(older_rec[0], older_rec[1], older_rec[2], older_rec[3]))

    diff_filenames_list.insert(0,'{}/recommendation.csv'.format(compact_diff_path))

    if len(older_filenames_list) != len(newer_filenames_list):
        raise Exception("Different Lengths of lists - Unacceptable")

    if diff_only_recommendation: length_to_iterate = 2  # SSSS and SSSSS
    else:                        length_to_iterate = len(newer_filenames_list)
    for index in range(length_to_iterate):
        if db_exists_in_both_folders == 0 and index == 0: continue
        output_csv_rows = [['ticker','change','from','to']]
        print("\n{:20}:\n==========================================================".format(newer_filenames_list[index]))

        # 1st, Read the Older File, which will be the reference:
        older_rows = []
        with open(older_filenames_list[index], mode='r', newline='') as engine:
            reader = csv.reader(engine, delimiter=',')
            row_index = 0
            for row in reader:
                if row_index == 0:
                    row_index += 1
                    continue
                else:
                    older_rows.append(row)
                    if row_index >= rec_length: break
                    row_index += 1

        # 2nd, read the Newer File and check if (and where) each line appears in the Older file (if at all)
        newer_rows = []
        with open(newer_filenames_list[index], mode='r', newline='') as engine:
            reader = csv.reader(engine, delimiter=',')
            row_index = 0
            for row in reader:
                if row_index == 0:
                    row_index += 1
                    continue
                else:
                    newer_rows.append(row)
                    ticker = row[ticker_index]
                    name   = row[name_index]
                    row_index_in_older_file = get_row_index(ticker_index, ticker, older_rows)
                    oldr = older_rows[row_index_in_older_file]
                    if row_index_in_older_file >= 0:
                        if abs(row_index_in_older_file - (row_index-1)) > movement_threshold:
                            print("{:10} ({:30}):  {:2} positions change from {:3} to {:3}".format(ticker, name, row_index_in_older_file-(row_index-1), row_index_in_older_file, (row_index-1)))
                            if not diff_only_recommendation:
                                print('                                                                                    From            sss_value: {:15}, ssss_value: {:15}, sssss_value: {:15}, ssse_value: {:15}, sssse_value: {:15}, ssssse_value: {:15}, sssi_value: {:15}, ssssi_value: {:15}, sssssi_value: {:15}, sssei_value: {:15}, ssssei_value: {:15}, sssssei_value: {:15}, enterprise_value_to_revenue: {:15}, evr_effective: {:15}, trailing_price_to_earnings: {:15}, enterprise_value_to_ebitda: {:15}, profit_margin: {:15}, annualized_profit_margin: {:15}, held_percent_institutions: {:15}, forward_eps: {:15}, trailing_eps: {:15}, price_to_book: {:15}, shares_outstanding: {:15}, net_income_to_common_shareholders: {:15}, nitcsh_to_shares_outstanding: {:15}, num_employees: {:15}, enterprise_value: {:15}, nitcsh_to_num_employees: {:15}, earnings_quarterly_growth: {:15}, price_to_earnings_to_growth_ratio: {:15}, sqrt_peg_ratio: {:15}, annualized_cash_flow_from_operating_activities: {:15}, ev_to_cfo_ratio: {:15}'.format(
                                                                                                                                           oldr[3],          oldr[4],           oldr[5],            oldr[6],           oldr[7],            oldr[8],             oldr[9],           oldr[10],           oldr[11],            oldr[12],           oldr[13],            oldr[14],             oldr[15],                           oldr[16],             oldr[17],                          oldr[18],                          oldr[19],             oldr[20],                        oldr[21],                         oldr[22],           oldr[23],            oldr[24],             oldr[25],                  oldr[26],                                 oldr[27],                            oldr[28],             oldr[29],                oldr[30],                       oldr[31],                         oldr[32],                                 oldr[33],              oldr[34],                                              oldr[35]))
                                print('                                                                                    To              sss_value: {:15}, ssss_value: {:15}, sssss_value: {:15}, ssse_value: {:15}, sssse_value: {:15}, ssssse_value: {:15}, sssi_value: {:15}, ssssi_value: {:15}, sssssi_value: {:15}, sssei_value: {:15}, ssssei_value: {:15}, sssssei_value: {:15}, enterprise_value_to_revenue: {:15}, evr_effective: {:15}, trailing_price_to_earnings: {:15}, enterprise_value_to_ebitda: {:15}, profit_margin: {:15}, annualized_profit_margin: {:15}, held_percent_institutions: {:15}, forward_eps: {:15}, trailing_eps: {:15}, price_to_book: {:15}, shares_outstanding: {:15}, net_income_to_common_shareholders: {:15}, nitcsh_to_shares_outstanding: {:15}, num_employees: {:15}, enterprise_value: {:15}, nitcsh_to_num_employees: {:15}, earnings_quarterly_growth: {:15}, price_to_earnings_to_growth_ratio: {:15}, sqrt_peg_ratio: {:15}, annualized_cash_flow_from_operating_activities: {:15}, ev_to_cfo_ratio: {:15}'.format(
                                                                                                                                           row[3],           row[4],            row[5],             row[6],            row[7],             row[8],              row[9],            row[10],            row[11],             row[12],            row[13],             row[14],              row[15],                            row[16],              row[17],                           row[18],                           row[19],              row[20],                         row[21],                          row[22],            row[23],             row[24],              row[25],                   row[26],                                  row[27],                             row[28],              row[29],                 row[30],                        row[31],                          row[32],                                  row[33],               row[34],                                               row[35] ))

                            output_csv_rows.append([ticker, row_index_in_older_file-(row_index-1), row_index_in_older_file, (row_index-1)])
                    else:
                        print("ticker {:10}: appears at position {:2} (new)".format(ticker, row_index-1))
                        if not diff_only_recommendation:
                            print('                                                                                                        sss_value: {:15}, ssss_value: {:15}, sssss_value: {:15}, ssse_value: {:15}, sssse_value: {:15}, ssssse_value: {:15}, sssi_value: {:15}, ssssi_value: {:15}, sssssi_value: {:15}, sssei_value: {:15}, ssssei_value: {:15}, sssssei_value: {:15}, enterprise_value_to_revenue: {:15}, evr_effective: {:15}, trailing_price_to_earnings: {:15}, enterprise_value_to_ebitda: {:15}, profit_margin: {:15}, annualized_profit_margin: {:15}, held_percent_institutions: {:15}, forward_eps: {:15}, trailing_eps: {:15}, price_to_book: {:15}, shares_outstanding: {:15}, net_income_to_common_shareholders: {:15}, nitcsh_to_shares_outstanding: {:15}, num_employees: {:15}, enterprise_value: {:15}, nitcsh_to_num_employees: {:15}, earnings_quarterly_growth: {:15}, price_to_earnings_to_growth_ratio: {:15}, sqrt_peg_ratio: {:15}, annualized_cash_flow_from_operating_activities: {:15}, ev_to_cfo_ratio: {:15}'.format(
                                                                                                                                           row[3],           row[4],            row[5],             row[6],            row[7],             row[8],              row[9],            row[10],            row[11],             row[12],            row[13],             row[14],              row[15],                            row[16],              row[17],                           row[18],                           row[19],              row[20],                         row[21],                          row[22],            row[23],             row[24],              row[25],                   row[26],                                  row[27],                             row[28],              row[29],                 row[30],                        row[31],                          row[32],                                  row[33],               row[34],                                               row[35] ))
                        output_csv_rows.append([ticker, 'new', 'new', (row_index - 1)])
                    if row_index >= rec_length: break
                    row_index += 1

        # 3rd, scan for Older File rows which do not appear in the Newer files anymore:
        row_index = 0
        for row in older_rows:
            ticker = row[ticker_index]
            row_index_in_newer_file = get_row_index(ticker_index, ticker, newer_rows)
            if row_index_in_newer_file < 0:
                print("ticker {:10}: disappeared from position {:2} (removed)".format(ticker, row_index))
                if not diff_only_recommendation:
                    print(           '                                                                                                    sss_value: {:15}, ssss_value: {:15}, sssss_value: {:15}, ssse_value: {:15}, sssse_value: {:15}, ssssse_value: {:15}, sssi_value: {:15}, ssssi_value: {:15}, sssssi_value: {:15}, sssei_value: {:15}, ssssei_value: {:15}, sssssei_value: {:15}, enterprise_value_to_revenue: {:15}, evr_effective: {:15}, trailing_price_to_earnings: {:15}, enterprise_value_to_ebitda: {:15}, profit_margin: {:15}, annualized_profit_margin: {:15}, held_percent_institutions: {:15}, forward_eps: {:15}, trailing_eps: {:15}, price_to_book: {:15}, shares_outstanding: {:15}, net_income_to_common_shareholders: {:15}, nitcsh_to_shares_outstanding: {:15}, num_employees: {:15}, enterprise_value: {:15}, nitcsh_to_num_employees: {:15}, earnings_quarterly_growth: {:15}, price_to_earnings_to_growth_ratio: {:15}, sqrt_peg_ratio: {:15}, annualized_cash_flow_from_operating_activities: {:15}, ev_to_cfo_ratio: {:15}'.format(
                                                                                                                                          row[3],           row[4],            row[5],             row[6],            row[7],             row[8],              row[9],            row[10],            row[11],             row[12],            row[13],             row[14],              row[15],                            row[16],              row[17],                           row[18],                           row[19],              row[20],                         row[21],                          row[22],            row[23],             row[24],              row[25],                   row[26],                                  row[27],                             row[28],              row[29],                 row[30],                        row[31],                          row[32],                                  row[33],               row[34],                                               row[35] ))
                output_csv_rows.append([ticker, 'removed', row_index, 'removed'])
            row_index += 1
        # Write results to CSV (if any changes detected):
        if len(output_csv_rows) > 1:
            os.makedirs(os.path.dirname(diff_filenames_list[index]), exist_ok=True)
            with open(diff_filenames_list[index], mode='w', newline='') as engine:
                writer = csv.writer(engine)
                writer.writerows(output_csv_rows)
