"""
Quickstart User Story Validation Script

This script validates all user stories from specs/001-mcp-server-prospect/quickstart.md
by testing the MCP tools through direct function calls (simulating AI assistant interactions).
"""
import asyncio
import os
import tempfile
import json
from pathlib import Path
from typing import Dict, Any, List

# Import MCP tools for testing
from src.mcp_server.tools import research_prospect, create_profile, get_prospect_data, search_prospects
from src.database.operations import init_db, list_prospects_default
from src.config import PROSPECTS_DIR, DATABASE_DIR

class UserStoryValidator:
    """Validates quickstart user stories through MCP tool testing."""
    
    def __init__(self):
        self.test_results = []
        self.test_companies = [
            "TechCorp Inc",
            "DataStream Inc", 
            "CloudSync Technologies",
            "StreamLine Software"
        ]
    
    def log_test(self, story: str, test_name: str, passed: bool, details: str = ""):
        """Log test result with details."""
        status = "✅ PASSED" if passed else "❌ FAILED"
        self.test_results.append({
            "story": story,
            "test": test_name,
            "status": status,
            "passed": passed,
            "details": details
        })
        print(f"{status}: {story} - {test_name}")
        if details:
            print(f"   Details: {details}")
    
    async def setup_test_environment(self):
        """Set up clean test environment."""
        print("🔧 Setting up test environment...")
        
        # Clean up any existing database files
        import shutil
        if DATABASE_DIR.exists():
            shutil.rmtree(DATABASE_DIR)
        DATABASE_DIR.mkdir(parents=True, exist_ok=True)
        
        # Clean up prospects directory
        if PROSPECTS_DIR.exists():
            shutil.rmtree(PROSPECTS_DIR)
        PROSPECTS_DIR.mkdir(parents=True, exist_ok=True)
        
        # Initialize fresh database
        await init_db()
        
        print("✅ Test environment ready")
    
    async def validate_story_1_complete_workflow(self):
        """Story 1: Complete 2-Step Prospect Research Workflow"""
        story = "Story 1: Complete 2-Step Workflow"
        
        test_company = "TechCorp Inc"
        
        try:
            # Step 1: Research
            print(f"\n🔍 Testing Step 1: Research for {test_company}")
            research_result = await research_prospect(company=test_company)
            
            # Validate research result
            research_success = isinstance(research_result, str) and len(research_result) > 0
            self.log_test(story, "Step 1 - Research Completion", research_success, 
                         f"Research result length: {len(research_result)} chars")
            
            if not research_success:
                return
            
            # Extract prospect_id from research result (it should mention the prospect ID)
            # For now, we'll use a standard format to find prospects
            prospects = await list_prospects_default()
            if not prospects:
                self.log_test(story, "Step 1 - Prospect Creation", False, "No prospects found in database")
                return
            
            # Get the most recently created prospect
            latest_prospect = max(prospects, key=lambda p: p.created_at)
            prospect_id = latest_prospect.id
            
            self.log_test(story, "Step 1 - Prospect Creation", True, 
                         f"Prospect created with ID: {prospect_id}")
            
            # Step 2: Profile Creation
            print(f"\n👤 Testing Step 2: Profile creation for prospect {prospect_id}")
            profile_result = await create_profile(prospect_id=prospect_id)
            
            profile_success = isinstance(profile_result, str) and len(profile_result) > 0
            self.log_test(story, "Step 2 - Profile Creation", profile_success,
                         f"Profile result length: {len(profile_result)} chars")
            
            # Validate files exist
            research_files = list(PROSPECTS_DIR.glob(f"*/*_research.md"))
            profile_files = list(PROSPECTS_DIR.glob(f"*/*_profile.md"))
            
            self.log_test(story, "File Generation - Research", len(research_files) > 0,
                         f"Research files found: {len(research_files)}")
            self.log_test(story, "File Generation - Profile", len(profile_files) > 0,
                         f"Profile files found: {len(profile_files)}")
            
            # Validate complete workflow
            workflow_complete = research_success and profile_success
            self.log_test(story, "Complete 2-Step Workflow", workflow_complete,
                         "Both research and profile steps completed successfully")
            
        except Exception as e:
            self.log_test(story, "Complete Workflow", False, f"Exception: {str(e)}")
    
    async def validate_story_2_step_by_step(self):
        """Story 2: Step-by-Step Workflow Execution"""
        story = "Story 2: Step-by-Step Execution"
        
        test_company = "DataStream Inc"
        
        try:
            # Individual step 1 test
            print(f"\n🔍 Testing individual Step 1 for {test_company}")
            research_result = await research_prospect(company=test_company)
            
            step1_success = isinstance(research_result, str) and "research" in research_result.lower()
            self.log_test(story, "Individual Step 1", step1_success,
                         f"Research initiated successfully")
            
            if step1_success:
                # Find the prospect for step 2
                prospects = await list_prospects_default()
                datastream_prospect = None
                for p in prospects:
                    if "datastream" in p.company_name.lower():
                        datastream_prospect = p
                        break
                
                if datastream_prospect:
                    # Individual step 2 test
                    print(f"\n👤 Testing individual Step 2 for prospect {datastream_prospect.id}")
                    profile_result = await create_profile(prospect_id=datastream_prospect.id)
                    
                    step2_success = isinstance(profile_result, str) and "profile" in profile_result.lower()
                    self.log_test(story, "Individual Step 2", step2_success,
                                 f"Profile created successfully")
                else:
                    self.log_test(story, "Individual Step 2", False, "DataStream prospect not found")
        
        except Exception as e:
            self.log_test(story, "Step-by-Step Execution", False, f"Exception: {str(e)}")
    
    async def validate_story_3_pipeline_management(self):
        """Story 3: Prospect Discovery and Pipeline Management"""
        story = "Story 3: Pipeline Management"
        
        try:
            print(f"\n📊 Testing pipeline management and search")
            
            # Test prospect search and status overview
            search_result = await search_prospects(query="")  # Empty query to get all
            
            search_success = isinstance(search_result, str) and len(search_result) > 0
            self.log_test(story, "Prospect Search", search_success,
                         f"Search returned {len(search_result)} chars of data")
            
            # Test specific company search
            tech_search = await search_prospects(query="TechCorp")
            tech_found = isinstance(tech_search, str) and "techcorp" in tech_search.lower()
            self.log_test(story, "Specific Company Search", tech_found,
                         "TechCorp found in search results")
            
            # Verify pipeline status can be determined
            prospects = await list_prospects_default()
            pipeline_status_available = len(prospects) > 0
            self.log_test(story, "Pipeline Status", pipeline_status_available,
                         f"Found {len(prospects)} prospects in pipeline")
            
        except Exception as e:
            self.log_test(story, "Pipeline Management", False, f"Exception: {str(e)}")
    
    async def validate_story_4_data_access(self):
        """Story 4: Accessing Prospect Intelligence"""
        story = "Story 4: Data Access"
        
        try:
            print(f"\n📄 Testing prospect data retrieval")
            
            # Get prospects to test data access
            prospects = await list_prospects_default()
            if not prospects:
                self.log_test(story, "Data Retrieval", False, "No prospects available for testing")
                return
            
            # Test get_prospect_data with first prospect
            test_prospect = prospects[0]
            prospect_data = await get_prospect_data(prospect_id=test_prospect.id)
            
            data_success = isinstance(prospect_data, str) and len(prospect_data) > 0
            self.log_test(story, "Prospect Data Retrieval", data_success,
                         f"Retrieved {len(prospect_data)} chars of prospect data")
            
            # Verify data contains key information
            has_company_info = test_prospect.company_name.lower() in prospect_data.lower()
            self.log_test(story, "Data Content Validation", has_company_info,
                         "Prospect data contains company information")
            
        except Exception as e:
            self.log_test(story, "Data Access", False, f"Exception: {str(e)}")
    
    async def validate_story_5_search_filtering(self):
        """Story 5: Prospect Search and Filtering"""
        story = "Story 5: Search and Filtering"
        
        try:
            print(f"\n🔍 Testing search and filtering capabilities")
            
            # Test content-based search
            api_search = await search_prospects(query="API")
            api_search_works = isinstance(api_search, str)
            self.log_test(story, "Content Search", api_search_works,
                         "API search completed successfully")
            
            # Test company name search  
            company_search = await search_prospects(query="TechCorp")
            company_search_works = isinstance(company_search, str)
            self.log_test(story, "Company Name Search", company_search_works,
                         "Company name search completed successfully")
            
            # Test empty search (should return all)
            all_search = await search_prospects(query="")
            all_search_works = isinstance(all_search, str) and len(all_search) > 0
            self.log_test(story, "All Prospects Search", all_search_works,
                         "Empty search returns all prospects")
            
        except Exception as e:
            self.log_test(story, "Search and Filtering", False, f"Exception: {str(e)}")
    
    async def validate_story_6_end_to_end(self):
        """Story 6: Complete End-to-End Workflow"""
        story = "Story 6: End-to-End Workflow"
        
        test_company = "CloudSync Technologies"
        
        try:
            print(f"\n🎯 Testing complete end-to-end workflow for {test_company}")
            
            # Complete workflow: Research + Profile + Data Access + Search
            research_result = await research_prospect(company=test_company)
            research_ok = isinstance(research_result, str) and len(research_result) > 0
            
            if research_ok:
                # Find the created prospect
                prospects = await list_prospects_default()
                cloudsync_prospect = None
                for p in prospects:
                    if "cloudsync" in p.company_name.lower():
                        cloudsync_prospect = p
                        break
                
                if cloudsync_prospect:
                    # Create profile
                    profile_result = await create_profile(prospect_id=cloudsync_prospect.id)
                    profile_ok = isinstance(profile_result, str) and len(profile_result) > 0
                    
                    if profile_ok:
                        # Get complete data
                        complete_data = await get_prospect_data(prospect_id=cloudsync_prospect.id)
                        data_ok = isinstance(complete_data, str) and len(complete_data) > 0
                        
                        # Search for the prospect
                        search_result = await search_prospects(query="CloudSync")
                        search_ok = isinstance(search_result, str) and "cloudsync" in search_result.lower()
                        
                        # Validate end-to-end workflow
                        end_to_end_success = research_ok and profile_ok and data_ok and search_ok
                        self.log_test(story, "Complete End-to-End Workflow", end_to_end_success,
                                     "Research → Profile → Data Access → Search all successful")
                        
                        # Check file generation
                        research_files = list(PROSPECTS_DIR.glob(f"*/*_research.md"))
                        profile_files = list(PROSPECTS_DIR.glob(f"*/*_profile.md"))
                        
                        files_generated = len(research_files) > 0 and len(profile_files) > 0
                        self.log_test(story, "File System Integration", files_generated,
                                     f"Research files: {len(research_files)}, Profile files: {len(profile_files)}")
                    else:
                        self.log_test(story, "Profile Creation", False, "Profile creation failed")
                else:
                    self.log_test(story, "Prospect Creation", False, "CloudSync prospect not found")
            else:
                self.log_test(story, "Research Initiation", False, "Research failed")
                
        except Exception as e:
            self.log_test(story, "End-to-End Workflow", False, f"Exception: {str(e)}")
    
    async def validate_performance_requirements(self):
        """Validate performance requirements from quickstart."""
        story = "Performance Validation"
        
        try:
            print(f"\n⚡ Testing performance requirements")
            
            import time
            
            # Test tool response time (<200ms requirement)
            start_time = time.time()
            search_result = await search_prospects(query="test")
            search_time = (time.time() - start_time) * 1000
            
            search_fast_enough = search_time < 200
            self.log_test(story, "Tool Response Time", search_fast_enough,
                         f"Search completed in {search_time:.1f}ms (< 200ms required)")
            
            # Test workflow completion time (<30s requirement)
            start_time = time.time()
            workflow_result = await research_prospect(company="Performance Test Co")
            workflow_time = time.time() - start_time
            
            workflow_fast_enough = workflow_time < 30
            self.log_test(story, "Workflow Completion Time", workflow_fast_enough,
                         f"Research workflow completed in {workflow_time:.1f}s (< 30s required)")
            
        except Exception as e:
            self.log_test(story, "Performance Validation", False, f"Exception: {str(e)}")
    
    async def validate_file_system_requirements(self):
        """Validate file system requirements from quickstart."""
        story = "File System Validation"
        
        try:
            print(f"\n📁 Testing file system requirements")
            
            # Check directory structure
            prospects_dir_exists = PROSPECTS_DIR.exists()
            self.log_test(story, "Prospects Directory", prospects_dir_exists,
                         f"Directory exists: {PROSPECTS_DIR}")
            
            database_dir_exists = DATABASE_DIR.exists()
            self.log_test(story, "Database Directory", database_dir_exists,
                         f"Directory exists: {DATABASE_DIR}")
            
            # Check for generated files
            research_files = list(PROSPECTS_DIR.glob(f"*/*_research.md"))
            profile_files = list(PROSPECTS_DIR.glob(f"*/*_profile.md"))
            
            files_exist = len(research_files) > 0 or len(profile_files) > 0
            self.log_test(story, "File Generation", files_exist,
                         f"Found {len(research_files)} research + {len(profile_files)} profile files")
            
            # Test file content quality
            if research_files:
                sample_file = research_files[0]
                file_size = sample_file.stat().st_size
                size_adequate = file_size > 1000  # At least 1KB
                self.log_test(story, "File Content Quality", size_adequate,
                             f"Sample research file size: {file_size} bytes")
            
        except Exception as e:
            self.log_test(story, "File System Validation", False, f"Exception: {str(e)}")
    
    def print_summary(self):
        """Print test summary with pass/fail counts."""
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r["passed"]])
        failed_tests = total_tests - passed_tests
        
        print(f"\n" + "="*60)
        print(f"🏁 QUICKSTART USER STORY VALIDATION SUMMARY")
        print(f"="*60)
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0:
            print(f"\n❌ FAILED TESTS:")
            for result in self.test_results:
                if not result["passed"]:
                    print(f"  - {result['story']}: {result['test']}")
                    if result["details"]:
                        print(f"    {result['details']}")
        
        print(f"\n✅ VALIDATION COMPLETE")
        
        # Return overall success
        return failed_tests == 0

async def main():
    """Run all quickstart user story validations."""
    print("🚀 Starting Quickstart User Story Validation")
    print("This validates all user stories from specs/001-mcp-server-prospect/quickstart.md")
    print("="*60)
    
    validator = UserStoryValidator()
    
    # Set up test environment
    await validator.setup_test_environment()
    
    # Run all user story validations
    await validator.validate_story_1_complete_workflow()
    await validator.validate_story_2_step_by_step()
    await validator.validate_story_3_pipeline_management()
    await validator.validate_story_4_data_access()
    await validator.validate_story_5_search_filtering()
    await validator.validate_story_6_end_to_end()
    
    # Run additional validations
    await validator.validate_performance_requirements()
    await validator.validate_file_system_requirements()
    
    # Print summary
    success = validator.print_summary()
    
    if success:
        print("🎉 All quickstart user stories validated successfully!")
        return 0
    else:
        print("⚠️  Some user story validations failed. See details above.")
        return 1

if __name__ == "__main__":
    import sys
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
