"""Test script to verify string IDs work correctly"""
from app.schemas import AssetReportCreate

# Test with string ID (like LP-1002)
test_data = {
    "asset_id": "LP-1002",
    "report_type": "Damaged",
    "description": "Screen flickering issue",
    "severity": "High"
}

try:
    report = AssetReportCreate(**test_data)
    print("✅ SUCCESS! Schema accepts string IDs")
    print(f"   Asset ID: {report.asset_id}")
    print(f"   Report Type: {report.report_type}")
    print(f"   Description: {report.description}")
    print(f"   Severity: {report.severity}")
except Exception as e:
    print(f"❌ FAILED: {e}")
