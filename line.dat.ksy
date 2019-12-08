meta:
  id: ms3dslevel
  file-extension: dat
  endian: le
  
seq:
  - id: seg1_collision
    type: segment
    doc: collision data
  - id: seg2_unk
    type: segment
  - id: seg3_unk
    type: segment
  - id: seg4_unk
    type: segment

types:
  point:
    seq:
      - id: x_coord
        type: u2le
      - id: y_coord
        type: u2le
  
  line:
    seq:
      - id: point1
        type: point
      - id: point2
        type: point
        
  element:
    seq:
      - id: unknown
        type: u2le
      - id: line
        type: line
  
  segment:
    seq:
      - id: length
        type: u1
      - id: elements
        type: element
        repeat: expr
        repeat-expr: length
      - id: terminator
        type: u1
      