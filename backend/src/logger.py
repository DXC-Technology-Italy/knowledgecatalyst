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
from google.cloud import logging as gclogger

class CustomLogger:
    def __init__(self):
        self.is_gcp_log_enabled = os.environ.get("GCP_LOG_METRICS_ENABLED", "False").lower() in ("true", "1", "yes")
        if self.is_gcp_log_enabled:
            self.logging_client = gclogger.Client()
            self.logger_name = "llm_experiments_metrics"
            self.logger = self.logging_client.logger(self.logger_name)
        else:
            self.logger = None

    def log_struct(self, message, severity="DEFAULT"):
        if self.is_gcp_log_enabled and message is not None:
            self.logger.log_struct({"message": message, "severity": severity})
        else:
            print(f"[{severity}]{message}")
