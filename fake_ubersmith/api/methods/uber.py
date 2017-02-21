# Copyright 2017 Internap.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from fake_ubersmith.api.base import Base
from fake_ubersmith.api.ubersmith import FakeUbersmithError
from fake_ubersmith.api.utils.helpers import record
from fake_ubersmith.api.utils.response import response


class Uber(Base):
    def __init__(self):
        super().__init__()

        self.records = {}
        self.service_plans = []
        self.service_plans_list = None
        self.service_plan_error = None

    def hook_to(self, entity):
        entity.register_endpoints(
            ubersmith_method='uber.service_plan_get',
            function=self.service_plan_get
        )
        entity.register_endpoints(
            ubersmith_method='uber.service_plan_list',
            function=self.service_plan_list
        )

    @record(method='plan.get')
    def service_plan_get(self, form_data):
        if isinstance(self.service_plan_error, FakeUbersmithError):
            return response(
               error_code=self.service_plan_error.code,
               message=self.service_plan_error.message
            )

        service_plan = next(
            (
                plan for plan in self.service_plans
                if plan["plan_id"] == form_data["plan_id"]
            ),
            None
        )

        if service_plan is not None:
            return response(data=service_plan)
        else:
            return response(
                error_code=3,
                message="No Service Plan found"
            )

    @record(method='plan.list')
    def service_plan_list(self, form_data):
        if 'code' in form_data:
            plan_code = form_data['code']
            return response(
                data={
                    plan['plan_id']: plan
                    for plan in self.service_plans_list.values()
                    if plan['code'] == plan_code
                }
            )
        return response(data=self.service_plans_list)
