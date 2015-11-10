# ------------- Modify these -------------
# ----------------------------------------

# install
install(DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/
  DESTINATION etc/${PROJECT_NAME}
  FILES_MATCHING PATTERN "*.odb"
  )
