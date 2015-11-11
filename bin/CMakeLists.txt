#
set(BINS
  app.py
  component.py
  idd.py
  inventory.py
  ipad.py
  module.py
  script.py
  service.py
  stationery.py
  table.py
  )

# journald.py conflict with journal/bin/journald.py
# rename
configure_file(
  journald.py
  pyre-journald.py
  )

# install
install(PROGRAMS ${BINS}
  DESTINATION bin
  )
install(PROGRAMS 
  ${CMAKE_CURRENT_BINARY_DIR}/pyre-journald.py
  DESTINATION bin
  )
