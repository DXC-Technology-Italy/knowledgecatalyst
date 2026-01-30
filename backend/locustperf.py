"""
SPDX-License-Identifier: AGPL-3.0-or-later
SPDX-FileCopyrightText: 2026 DXC Technology Company

KnowledgeCatalyst - Knowledge Graph RAG System
Copyright (C) 2026 DXC Technology Company

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
"""

import os
import time
from locust import HttpUser, TaskSet, task, between, events
from requests.auth import HTTPBasicAuth
import json

# Global variables to store results
results = {
    "total_requests": 0,
    "total_failures": 0,
    "response_times": []
}

class UserBehavior(TaskSet):

    @task
    def post_request(self):
        payload = {
            "uri": "",
            "database": "",
            "userName": ""
        }
        with self.client.post("/connect", json=payload, catch_response=True) as response:
            # https://prod-backend-dcavk67s4a-uc.a.run.app/connect
            results["total_requests"] += 1
            if response.status_code == 200:
                results["response_times"].append(response.elapsed.total_seconds())
            else:
                results["total_failures"] += 1
                response.failure("Failed POST request")
    
    @task
    def get_request(self):
        with self.client.get("/health", catch_response=True) as response:
            results["total_requests"] += 1
            if response.status_code == 200:
                results["response_times"].append(response.elapsed.total_seconds())
            else:
                results["total_failures"] += 1
                response.failure("Failed GET request")

    @task
    def get_request(self):
        with self.client.get("/sources_list", catch_response=True) as response:
            results["total_requests"] += 1
            if response.status_code == 200:
                results["response_times"].append(response.elapsed.total_seconds())
            else:
                results["total_failures"] += 1
                response.failure("Failed GET request")

    # @task(4)
    # def upload_file(self):
    #     files = {
    #         "file": ("filename.txt", open("filename.txt", "rb"), "text/plain")
    #     }
    #     with self.client.post("/your-upload-endpoint", files=files, catch_response=True) as response:
    #         results["total_requests"] += 1
    #         if response.status_code == 200:
    #             results["response_times"].append(response.elapsed.total_seconds())
    #         else:
    #             results["total_failures"] += 1
    #             response.failure("Failed UPLOAD request")

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(5, 15)

@events.quitting.add_listener
def generate_summary(environment, **kwargs):
    total_requests = results["total_requests"]
    total_failures = results["total_failures"]
    avg_response_time = sum(results["response_times"]) / len(results["response_times"]) if results["response_times"] else 0

    summary = {
        "total_requests": total_requests,
        "total_failures": total_failures,
        "average_response_time": avg_response_time
    }

    print("\nPerformance Test Summary:")
    print(json.dumps(summary, indent=4))

if __name__ == "__main__":
    os.system("locust -f locustperf.py")