#
# Created by Qingzhi Ma on Wed May 13 2020
#
# Copyright (c) 2020 Department of Computer Science, University of Warwick
# Copyright 2020 Qingzhi Ma
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import unittest

from dbestclient.executor.executor import SqlExecutor


class TestHw(unittest.TestCase):
    def test_cpu(self):
        sqlExecutor = SqlExecutor()
        sqlExecutor.execute("create table hw(usermac categorical , ts real,tenantId categorical, ssid  categorical,kpiCount categorical,regionLevelEight categorical)  "  #
                            "FROM '/home/u1796377/Documents/workspace/DBEstClient/tests/integration/fixtures/sample_1k.csv' "
                            "GROUP BY ts "
                            "method uniform "
                            "size  1000 "  # 118567, 81526479
                            "scale data;", device='cpu')
        predictions = sqlExecutor.execute("select ts, count(usermac) from hw "
                                          "where   unix_timestamp('2020-02-05T12:00:00.000Z') <=ts<= unix_timestamp('2020-04-06T12:00:00.000Z') "
                                          "AND tenantId = 'default-organization-id' "
                                          "AND ssid = 'Tencent' "
                                          "AND kpiCount >=1  "
                                          "AND regionLevelEight='287d4300-06bb-11ea-840e-60def3781da5'"
                                          "GROUP BY ts;", n_jobs=1, device='cpu')
        # print("predictions", predictions)
        self.assertTrue(abs(predictions['1583402400000']-316.683) < 10)


class TestTpcDs(unittest.TestCase):
    def test_categorical(self):
        sqlExecutor = SqlExecutor()
        sqlExecutor.execute("set b_grid_search='False'")
        sqlExecutor.execute("set csv_split_char='|'")
        sqlExecutor.execute("set table_header=" +
                            "'ss_sold_date_sk|ss_sold_time_sk|ss_item_sk|ss_customer_sk|ss_cdemo_sk|ss_hdemo_sk|" +
                            "ss_addr_sk|ss_store_sk|ss_promo_sk|ss_ticket_number|ss_quantity|ss_wholesale_cost|" +
                            "ss_list_price|ss_sales_price|ss_ext_discount_amt|ss_ext_sales_price|" +
                            "ss_ext_wholesale_cost|ss_ext_list_price|ss_ext_tax|ss_coupon_amt|ss_net_paid|" +
                            "ss_net_paid_inc_tax|ss_net_profit|none'"
                            )
        sqlExecutor.execute(
            "create table ss40g(ss_sales_price real, ss_sold_date_sk real, ss_coupon_amt categorical) from '/data/tpcds/40G/ss_600k.csv' GROUP BY ss_store_sk method uniform size 600 scale data num_of_points2.csv", device='cpu', n_jobs=1)
        predictions = sqlExecutor.execute(
            "select avg(ss_sales_price)  from ss40g where   2451119  <=ss_sold_date_sk<= 2451483 and ss_coupon_amt=''  group by ss_store_sk", n_jobs=1, device='cpu')
        self.assertTrue(predictions)


if __name__ == "__main__":
    unittest.main()